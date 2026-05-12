from enum import Enum


class LogType(Enum):
    DBMODEL = "DBModel"
    MONGO_CALL = "MongoDB Call"
    OTHER = "Other"


class Color(Enum):
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

class Logger():
    DISALLOWED_LOG_TYPES = [
        LogType.DBMODEL,
        LogType.MONGO_CALL
    ]

    @staticmethod
    def log(message: str, log_type: LogType = LogType.OTHER):
        if log_type in Logger.DISALLOWED_LOG_TYPES:
            return

        prefix = log_type.value
        print(f"[{prefix}]: {message}")

    @staticmethod
    def warn(message: str, log_type: LogType = LogType.OTHER):
        prefix = log_type.value
        print(f"{Color.YELLOW.value}[WARN] [{prefix}]{Color.END.value}: {message}")
