import redis

redisClient = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

print(redisClient.ping())

TASK_QUEUE = "task_queue"

redisClient.lpush(TASK_QUEUE, "aaaaaaaaaaa")

def wait_and_pop():
    entry = redisClient.brpop(TASK_QUEUE)
    return entry[1]

if __name__ == "__main__":
    print(wait_and_pop())