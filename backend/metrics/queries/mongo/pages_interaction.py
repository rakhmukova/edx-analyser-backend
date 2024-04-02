import time
from typing import Any

from metrics.queries.mongo.mongo_connection import MongoConnection
from metrics.utils.url_operations import remove_parameters_from_url


def calc_pages_interaction(collection, course_id) -> list[Any]:
    pipeline = [
        {
            "$group": {
                "_id": "$page",
                "interaction_count": {"$sum": 1}
            }
        },
        {
            "$sort": {"interaction_count": -1}
        }
    ]

    return collection.aggregate(pipeline)


if __name__ == '__main__':
    client = MongoConnection()
    collection = client.collection

    start_time = time.time()
    results = calc_pages_interaction(collection, "course-v1:ITMOUniversity+DATANTECH2035+summer_2022_1")
    end_time = time.time()
    for result in results:
        print(remove_parameters_from_url(result["_id"]), result["interaction_count"])
    print(f"Execution time: {end_time - start_time} seconds")

    # group by again
