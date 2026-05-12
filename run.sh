container_name="tab_cleaner_mongodb"

start() {
		echo "Starting Mongo container..."
		docker start $container_name
}

cleanup() {
		echo "Complete! Stopping container."
		docker stop $container_name	
}

trap cleanup EXIT INT TERM

if docker ps | grep -q "$container_name"; then
		echo "Container already started."
else
		start
fi

python main.py


