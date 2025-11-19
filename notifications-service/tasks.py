from celery import Celery

app = Celery('tasks', broker='redis://redis:6379/0')

@app.task
def send_email_notification(user_id, message):
    print(f"Sending email to user {user_id}: {message}")