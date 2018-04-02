from .celery import app

@app.task
def send_email_async(send_type="send"):
	print('邮箱发送成功+1')

