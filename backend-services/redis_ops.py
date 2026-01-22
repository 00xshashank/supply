import redis

redisClient = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

# print(redisClient.ping())

TASK_QUEUE = "task_queue"

def wait_and_pop():
    entry = redisClient.brpop(TASK_QUEUE)
    return entry[1]

def set_status(project_id: str, status: str):
    redisClient.hset(name='status', key=project_id, value=status)

if __name__ == "__main__":
    print(wait_and_pop())