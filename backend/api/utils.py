import math
import random

def generate_random_id(l: int):
    vocab = "abcdefghijklmnopqrstuvwxyz134567890"
    id = ""
    for _ in range(l):
        id += vocab[math.floor(random.random()*(len(vocab)-1))]
    return id