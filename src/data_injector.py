import psycopg
from faker import Faker
from tqdm import trange

from config.settings import settings


def inject_data(amount_of_records: int = 1000, batch_size: int = 100) -> None:
    iterations = amount_of_records // batch_size
    fake = Faker()
    with (
        psycopg.connect(**settings.database.model_dump(by_alias=True)) as conn,
        conn.cursor() as cur,
    ):
        for _ in trange(iterations, desc=f"Injecting {amount_of_records} records"):
            batch = []
            for _ in range(batch_size):
                batch.append((fake.name(), fake.text()))
            cur.executemany(
                "insert into movies (title, description) values (%s, %s)", batch
            )


if __name__ == "__main__":
    inject_data(100_000)
