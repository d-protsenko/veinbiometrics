MONGO_DB_CONTAINER_NAME=vebio_mongo
DB_NAME=vebio_db
DB_USER=vebio_user
DB_USER_PWD=vebio_password
AUTH_DB=admin


.PHONY: acquisition

preprocess:
	python preprocessImage.py -in ${input} -out ${output}


.PHONY: init_db

init_db:
	docker-compose up -d

.PHONY: connect-to-db

connect-to-db:
	docker exec -it ${MONGO_DB_CONTAINER_NAME} bash -c "mongo --username ${DB_USER} --password ${DB_USER_PWD} --authenticationDatabase ${AUTH_DB} mongodb://localhost:27017/${DB_NAME}"

.PHONY: start_server

start_server:
	python ./biometrics/manage.py runserver 8080