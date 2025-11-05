run:
	docker compose -f docker-compose.yml up --build

exec:
	docker compose -f docker-compose.yml exec web sh

run_prod:
	docker-compose -f docker-compose.prod.yml up -d --build

exec_prod:
	docker-compose -f docker-compose.prod.yml exec web sh
