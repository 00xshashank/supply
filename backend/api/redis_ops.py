import redis

redisClient = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

TASK_QUEUE = "task_queue"

def queue_task(project_id: str):
    return redisClient.lpush(TASK_QUEUE, project_id)