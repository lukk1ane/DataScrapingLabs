import time
import random

def smart_delay(short=True):
    if short:
        time.sleep(random.uniform(1, 3))
    else:
        time.sleep(random.uniform(3, 6))

def get_star_rating(class_str):
    stars = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }
    for word in stars:
        if word in class_str:
            return stars[word]
    return 0
