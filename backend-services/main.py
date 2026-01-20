import redis

# Create Redis Client
redisClient = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

print(redisClient.ping())

TASK_QUEUE = "task_queue"

redisClient.lpush(TASK_QUEUE, "696f0c3c6f6b2d752d53da9b")
entry = redisClient.brpop(TASK_QUEUE)
print(entry)

while True:
    break