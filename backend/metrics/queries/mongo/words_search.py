import time

from metrics.queries.mongo.mongo_connection import MongoConnection


def calc_words_search_count(collection, course_id):
    pipeline = [
        {
            "$group": {
                "_id": "$decoded_event.query",
                "search_count": {"$sum": 1}
            }
        },
        {
            "$sort": {"search_count": -1}
        }
    ]

    return collection.aggregate(pipeline)


# None 1113148
# Execution time: 9.36560583114624 seconds
if __name__ == '__main__':
    client = MongoConnection()
    collection = client.collection

    start_time = time.time()
    results = calc_words_search_count(collection, "course-v1:ITMOUniversity+DATANTECH2035+summer_2022_1")
    end_time = time.time()
    for result in results:
        print(result["_id"], result["search_count"])
    print(f"Execution time: {end_time - start_time} seconds")