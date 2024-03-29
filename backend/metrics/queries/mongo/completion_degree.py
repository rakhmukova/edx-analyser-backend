import time

from metrics.queries.mongo.mongo_connection import MongoConnection


# pipeline = [
#     {
#         "$match": {
#             "event_type": "edx.special_exam"
#         }
#     },
#     {
#         "$group": {
#             "_id": "$context.user_id",
#             "user_id": {"$first": "$context.user_id"},
#             "finished": {
#                 "$sum": {
#                     "$cond": [
#                         {"$eq": ["$event_type", "edx.special_exam_completed"]},
#                         1,
#                         0
#                     ]
#                 }
#             }
#         }
#     },
#     {
#         "$project": {
#             "_id": 0,
#             "user_id": 1,
#             "finished": {
#                 "$cond": [
#                     {"$gt": ["$finished", 0]},
#                     "finished",
#                     "not_finished"
#                 ]
#             }
#         }
#     }
# ]

def get_enrolled_user_ids(database, course_id):
    pipeline = [
        {
            "$match": {
                "event_type": "edx.course.enrollment.activated",
                "event.course_id": course_id
            }
        },
        {
            "$group": {
                "_id": "$event.user_id",
            }
        }
    ]

    return database.all_logs.aggregate(pipeline)


if __name__ == '__main__':
    client = MongoConnection()
    db = client.database

    start_time = time.time()
    results = get_enrolled_user_ids(db, "course-v1:ITMOUniversity+DATANTECH2035+summer_2022_1")
    end_time = time.time()
    for result in results:
        print(result["_id"])
    print(f"Execution time: {end_time - start_time} seconds")

# all enrolled
#
# finished - those who completed exam
# started not finished - has active sessions
# not started - the rest
