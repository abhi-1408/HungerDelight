from celery import Celery


app = Celery('project', backend='rpc://',
             broker='amqp://guest@localhost//',
             include=['project.tasks']
             )

if __name__ == '__main__':
    app.start()
    app.autodiscover_tasks()
