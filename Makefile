install:
	docker build -t clara-bot .
	docker run --name clara --rm clara-bot

run:
	docker run --name clara --rm clara-bot

sh:
	 docker exec -it clara "/bin/sh"

.PHONY: install