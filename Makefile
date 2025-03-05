.PHONY: help
help: ## Help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort -d | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

.PHONY: create-venv
create-venv: ## create venv and install dependencies
	uv sync

.PHONY: start-db
start-db: ## start postgres
	docker compose up -d

.PHONY: run-inject
run-inject: ## run data injector
	cd src && uv run python ./data_injector.py

.PHONY: start-etl
start-etl: ## start etl process
	cd src && uv run python main.py

.PHONY: stop-db
stop-db-clear: ## stop postgres and clear all
	docker compose down -v


.PHONY: transfer-data
transfer-data: ## transfer data from sqlite
	cd 03_sqlite_to_postgres && python load_data.py

.PHONY: wait_to_db
wait_to_db:
	bash -c "until docker exec etl_coro_db pg_isready ; do echo 'db is starting...' ; sleep 1 ; echo 'db is up' ; done"

start-all: create-venv start-db wait_to_db run-inject start-etl
