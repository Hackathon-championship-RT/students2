help:
  @awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

start: ## Application start
	echo 'starting'
	docker-compose -f ./docker-compose.local.yaml up -d --build
	

stop: ## Application stop
	echo 'stopping'
	docker-compose -f ./docker-compose.local.yaml down

restart: stop
	$(MAKE) start
