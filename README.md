# AutoMahjong

## Features:
+ Play Mahjong with car manufacture tiles
+ Pick between retro/electric/all cars
+ Pick between different difficulty levels
+ See results on the leaderboard
+ See short description of car brands (In progress)

## Technologies:
+ Python 3.12, Poetry
+ FastAPI
+ React
+ PostgreSQL
+ SQLalchemy
+ Alembic
+ Docker
+ JWT
+ Ruff

## Running

Create .env file
```bash
cp .env-example, .env
```

### With Docker:
```bash
docker-compose -f docker-compose.local.yaml up
```

### Locally:
1. Install Python 3.12 and Poetry
2. Install dependencies
    ```bash
    poetry install
    ```
3. Start database
    ```bash
    docker-compose -f docker-compose.local.yaml up postgres
    ```
4. Apply database migrations
    ```bash
    poetry run alembic upgrade head
    ```
5. Run API
    ```bash
    poetry run python src/api/webserver.py
    ```

### Locally via make:
```bash
make start
```

To run from Docker set `POSTGRES_HOST = postgres`, `localhost` otherwise
