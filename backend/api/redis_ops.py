import redis

redisClient = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)

TASK_QUEUE = "task_queue"
STATUS_QUEUE = "status"

def queue_task(project_id: str):
    return redisClient.lpush(TASK_QUEUE, project_id)

def get_task_status(project_id: str):
    return redisClient.hget("status", project_id)
