from datetime import datetime
from time import sleep
from typing import Generator

import psycopg
from psycopg import ServerCursor
from psycopg.conninfo import make_conninfo
from psycopg.rows import class_row

from config.settings import settings
from models.models import Movie
from state.json_file_storage import JsonFileStorage
from state.state import State
from utils.decorators import coroutine
from utils.logger import logger

STATE_KEY = "last_movies_updated"


@coroutine
def fetch_changed_movies(
    cursor: ServerCursor[Movie], next_node: Generator[None, list[Movie], None]
) -> Generator[None, datetime, None]:
    while last_updated := (yield):
        logger.info(f"Fetching movies changed after %s", last_updated)
        cursor.execute(
            "SELECT * FROM movies WHERE updated_at > %s order by updated_at asc",
            (last_updated,),
        )
        while results := cursor.fetchmany(size=100):
            next_node.send(results)


@coroutine
def transform_movies(
    next_node: Generator[None, list[Movie], None],
) -> Generator[None, list[Movie], None]:
    while movies := (yield):
        logger.info("Received for transform %s movies", len(movies))
        for movie in movies:
            movie.title = movie.title.upper()
            logger.info(movie.model_dump_json())
        next_node.send(movies)


@coroutine
def save_movies(state: State) -> Generator[None, list[Movie], None]:
    while movies := (yield):
        logger.debug("Received for saving %s movies", len(movies))
        print([movie.model_dump_json() for movie in movies])
        state.set_state(STATE_KEY, str(movies[-1].updated_at))


def run_etl_process() -> None:
    state = State(JsonFileStorage(logger=logger))

    dsn = make_conninfo(**settings.database.model_dump(by_alias=True))
    print(dsn)

    with (
        psycopg.connect(dsn, row_factory=class_row(Movie)) as conn,
        ServerCursor(conn, "fetcher") as cur,
    ):
        saver_coro = save_movies(state)
        transformer_coro = transform_movies(next_node=saver_coro)
        fetcher_coro = fetch_changed_movies(cursor=cur, next_node=transformer_coro)

        while True:
            last_movies_updated = state.get_state(STATE_KEY) or str(datetime.min)
            logger.info(
                f"Starting ETL process for updates from %s ...", last_movies_updated
            )

            fetcher_coro.send(last_movies_updated)

            sleep(15)


if __name__ == "__main__":
    run_etl_process()
