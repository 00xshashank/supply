import math
import random

def generate_random_id(len: int):
    vocab = "abcdefghijklmnopqrstuvwxyz134567890"
    id = ""
    for _ in range(len):
        id += vocab[math.floor(random.random()*(len(vocab)-1))]
    return id