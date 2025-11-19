from celery import Celery

celery_app = Celery(
    "chat_service",
    broker="redis://redis:6379/0"
)

def notify_users(room_members, message):
    for user_id in room_members:
        celery_app.send_task(
            "tasks.send_email_notification",  # task name in notifications-service
            args=[user_id, message]
        )
