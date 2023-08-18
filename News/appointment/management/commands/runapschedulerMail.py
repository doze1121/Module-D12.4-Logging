#ЗАДАНИЕ 6.5.1 НА САМОПРОВЕРКУ
#Напишите команду, которая будет отправлять письма на вашу почту раз в 10 секунд. 
#Содержание письма остаётся на ваш выбор, но желательно как-то добавить опознавательный знак, 
#что письмо было отправлено именно из Django, чтобы вы не запутались.

# python manage.py runapschedulerMail

import logging
 
from django.conf import settings
 
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
 
from django.core.mail import send_mail
 
 
logger = logging.getLogger(__name__)
 
 
def my_job():
    send_mail(
        'Сообщение из Django по модулю 6.5',
        'Привет! Каждые 10 сек приходит тебе это сообщение))))))',
        from_email='sandrasandra0112@yandex.ru',
        recipient_list=['sandrasandra0112@mail.ru'],
    )
 
 
def delete_old_job_executions(max_age=604_800):
    """This job deletes all apscheduler job executions older than `max_age` from the database."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)
 
 
class Command(BaseCommand):
    help = "Runs apscheduler."
 
    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # добавляем работу нашему задачнику
        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/10"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")
 
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )
 
        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")