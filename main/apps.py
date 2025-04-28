from django.apps import AppConfig
import os
import logging

class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        if os.environ.get('RUN_MAIN') != 'true':
            return

        from apscheduler.schedulers.background import BackgroundScheduler
        from apscheduler.triggers.interval import IntervalTrigger
        from django_apscheduler.jobstores import DjangoJobStore
        from main.tasks import send_event_reminders

        scheduler = BackgroundScheduler()
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            send_event_reminders,
            trigger=IntervalTrigger(minutes=1),
            id="send_event_reminders",
            replace_existing=True,
        )

        try:
            scheduler.start()
            logging.getLogger(__name__).info("Scheduler started.")
        except Exception as e:
            logging.getLogger(__name__).error(f"Scheduler failed: {e}")