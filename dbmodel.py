from typing import ClassVar, Type, TypeVar, Optional, Union, get_args, get_origin, List
from bson import ObjectId
from pydantic import BaseModel, Field
from pymongo.collection import Collection
from db import db
from logger import LogType, Logger



DBModelType = TypeVar("DBModelType", bound="DBModel")


class ModelException(Exception):
    def __init__(self, message: str):
            self.message = message

    def __str__(self):
        return f"ModelException: {self.message}"


class DBModel(BaseModel):
    # All MongoDB models have an _id UUID.
    # It's stored as an ObjectId, but we'll turn that into a string when reading/writing from/to the DB.
    id: str = Field(default_factory = lambda: str(ObjectId()))
    # TODO: Subclasses must implement this!!!
    __collection_name__: ClassVar[str]

    @classmethod
    def _get_collection(cls: Type[DBModelType]) -> Collection:
        return db[cls.__collection_name__]

    @classmethod
    def map_obj(cls: Type[DBModelType], obj: dict, populate: bool) -> Optional[Union[DBModelType, dict]]:
        """
        populate (bool):
        - True =>
            - Expects all fields w/ DBModel types, or wrapped DBModel types,
            to be/have string IDs as values. Each DB model is retrieved from the DB,
            and the resulting dict is populated with these models.
            - Use populate=True for going from raw DB dict -> object.
            - Queries DB for DB model fields' values.

        - False =>
            - Expects all fields w/ DBModel types, or wrapped DBModel types,
            to be/have DBModel objects as values. Each value is mapepd to its ID,
            and the resulting dict is unpopulated.
            - Use populate=False for going from object -> raw DB dict.
            - Creates all DB model fields!
        """

        modified_fields = {} # field name -> modified values
        for field_name, field in cls.model_fields.items():
            origin = get_origin(field.annotation)

            # Handle field wrapped type is DB model
            if str(origin) == "<class 'list'>":
                wrapped_type = get_args(field.annotation)[0]
                is_db_model = issubclass(wrapped_type, DBModel)

                if is_db_model:
                    if populate:
                        value_ids: List[str] = obj[field_name]
                        values: List[DBModel] = []
                        for id in value_ids:
                            val = wrapped_type.find(id)
                            if val is None:
                                print("WTF VAL IS NONE!")
                            else:
                                values.append(val)
                        modified_fields[field_name] = values
                    else:
                        value_ids: List[str] = []
                        values: List[DBModel] = obj[field_name]
                        for value in values:
                            if wrapped_type.find(value.id) is None:
                                # print("Creating value...")
                                # print(value)
                                value.create()
                                value_ids.append(value.id)
                            else:
                                # print("Value already exists!")
                                value_ids.append(value.id)

                        modified_fields[field_name] = value_ids
            # Handle field type is DB model
            elif origin is None:
                field_type = field.annotation
                if field_type is None:
                    Logger.warn("field.annotation is None in map_obj; this is an unknown/unexpected case.", LogType.DBMODEL)
                    continue

                if not issubclass(field_type, DBModel):
                    continue

                field_value = obj[field_name]
                if populate:
                    # dict + IDs -> object
                    val = field_type.find(field_value)
                    if val is None:
                        print("WTF VAL IS NONE!")
                        raise Exception()
                    modified_fields[field_name] = val
                else:
                    # object -> dict + IDs, and create anything needed in the process
                    if field_type.find(field_value.id) is None:
                        field_value.create()

                    modified_fields[field_name] = field_value.id
            # Handle wrapped type is DB model, but wrapper is not list
            else:
                Logger.warn("Handling non-list wrapper types of wrapped DBModels is unimplemented.", LogType.DBMODEL)
                # Handle unions, optional etc.
                modified_fields[field_name] = obj[field_name]
                pass

        for field_name, field_value in modified_fields.items():
            obj[field_name] = field_value

        return cls.parse_obj(obj) if populate else obj

    # Takes in a dict -> returns the populated object.
    @classmethod
    def populate_obj(cls: Type[DBModelType], obj: dict) -> Optional[DBModelType]:
        Logger.log(f"{cls.__class__.__name__}.populate_obj(...)", LogType.DBMODEL)
        return cls.map_obj(obj, populate=True)

    @classmethod
    def depopulate_obj_for_db(cls: Type[DBModelType], obj: dict) -> Optional[dict]:
        Logger.log(f"{cls.__class__.__name__}.depopulate_obj_for_db(...)", LogType.DBMODEL)
        return cls.map_obj(obj, populate=False)

    @classmethod
    def replace_db_id_for_obj(cls: Type[DBModelType], item: dict) -> dict:
        """
        Replace db model's ObjectId with string
        """

        item["id"] = str(item["_id"])
        del item["_id"]
        return item

    @classmethod
    def replace_obj_id_for_db(cls: Type[DBModelType], item: dict) -> dict:
        """
        Replace object's (as dict) ID field with ObjectId
        """

        item["_id"] = ObjectId(item["id"])
        del item["id"]
        return item

    @classmethod
    def query(cls: Type[DBModelType], query: dict) -> Optional[DBModelType]:
        Logger.log(f"{cls.__name__}.query()", LogType.DBMODEL)
        result = cls._get_collection().find_one(query)

        if result is None: return None

        result = cls.replace_db_id_for_obj(result)
        populated_obj = cls.populate_obj(result)

        return populated_obj

    @classmethod
    def find(cls: Type[DBModelType], id: str) -> Optional[DBModelType]:
        Logger.log(f"{cls.__name__}.find()", LogType.DBMODEL)
        result = cls._get_collection().find_one({
            "_id" : ObjectId(id)
        })

        if result is None: return None

        result = cls.replace_db_id_for_obj(result)
        populated_obj = cls.populate_obj(result)

        return populated_obj

    # TODO: Test this method; test that population is right/working.
    # Seems to work for the simple AccessToken, which isn't a nested DBModel.
    @classmethod
    def find_all(cls: Type[DBModelType]) -> List[DBModelType]:
        Logger.log(f"{cls.__name__}.find_all()", LogType.DBMODEL)
        raw_result = cls._get_collection().find()

        items = []
        for item in raw_result:
            result = cls.replace_db_id_for_obj(item)
            populated_obj = cls.populate_obj(result)
            items.append(populated_obj)

        return items



    def create(self):
        Logger.log(f"{self.__class__.__name__}.create()", LogType.DBMODEL)
        copy = dict(self)

        copy = self.__class__.replace_obj_id_for_db(copy)
        depopulated_dict = self.__class__.depopulate_obj_for_db(copy)
        print(type(depopulated_dict))

        Logger.log(f"{self.__class__.__name__}.create() – insert_one", LogType.MONGO_CALL)
        self.__class__._get_collection().insert_one(depopulated_dict)

    def save(self):
        """
        Save changes to a model (in Mongo).
        """
        Logger.log(f"{self.__class__.__name__}.save()", LogType.DBMODEL)

        if self.find(self.id) is None:
            raise ModelException(f"Tried to save model with id {self.id}, but model doesn't exist in DB. Create model first/instead with DBModel.create().")

        copy = dict(self)

        copy = self.__class__.replace_obj_id_for_db(copy)
        depopulated_dict = self.__class__.depopulate_obj_for_db(copy)

        self.__class__._get_collection().update_one({ "_id" : ObjectId(self.id)}, { "$set": depopulated_dict }, upsert=False)

    # TODO: Implement recursive delete
    def delete(self, recursive: bool):
        """
        Delete self's model (from Mongo).
        """
        Logger.log(f"{self.__class__.__name__}.delete()", LogType.DBMODEL)
        self.__class__._get_collection().delete_one({"_id":ObjectId(self.id)})

        if not recursive: return
