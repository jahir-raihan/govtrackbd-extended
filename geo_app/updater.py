from apscheduler.schedulers.background import BackgroundScheduler
from .algorithms import *


def start():

    """To update projects database automatically"""

    scheduler = BackgroundScheduler()
    scheduler.add_job(update_ndre_projects_data, 'interval', minutes=1000)
    scheduler.add_job(update_lged_projects_data, 'interval', minutes=1440)
    scheduler.start()