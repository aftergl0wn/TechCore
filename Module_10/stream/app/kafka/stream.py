import json
import os

import faust
from dotenv import load_dotenv

load_dotenv(".env")

app = faust.App(
    "analytics-streaming",
    broker=os.getenv("KAFKA_BOOTSTRAP_SERVERS"),
    store="memory://",
)

book_views_topic = app.topic("book_views", value_type=bytes)


views_table = app.Table(
    "views_count",
    default=int,
).tumbling(60.0, expires=10.0)


@app.agent(book_views_topic)
async def count_views(stream: faust.Stream[bytes]) -> None:
    async for event in stream:
        payload = json.loads(event.decode("utf-8"))
        book_id = payload.get("book_id")

        if book_id is not None:
            views_table[book_id] += 1

            current_count = views_table[book_id]
            msg = (
                f"Просмотры книги {book_id}: {current_count}"
            )
            print(msg)


if __name__ == "__main__":
    app.main()
