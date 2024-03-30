import random

def throw_exception_with_probability(probability):
    if random.random() < probability:
        raise Exception(f"Exception occurred with probability {probability}")
