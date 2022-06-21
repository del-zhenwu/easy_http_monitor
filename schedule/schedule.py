import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.mongodb import MongoDBJobStore
from task import task_runner
from config import Config

config = Config()
logger = logging.getLogger("easy_http.schedule.schedule")

# executors = {
#     "default": ThreadPoolExecutor(10),
# }



class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class SchedulerWrapper(object):
    # __metaclass__ = Singleton

    def __init__(self, mode):
        if mode == "scanner":
            self.collection_name = "scanner_job"
        elif mode == "alerter":
            self.collection_name = "alerter_job"
        self.mode = mode
        job_stores = {
            "default": MongoDBJobStore(
                collection=self.collection_name,
                database=config.MONGODB_NAME,
                host=config.MONGODB_HOST,
                port=config.MONGODB_PORT)}
        job_defaults = {
                # "coalesce": False,
                "max_instances": 3}
        self.sdu = BackgroundScheduler(jobstores=job_stores, job_defaults=job_defaults)

    def add_job(self, job_id=None, seconds=None, **kwargs):
        logger.info("New schedule job[%s]: interval [%d]" % (job_id, seconds))
        args = [self.mode, kwargs["http_config"]]
        job = self.sdu.add_job(
            task_runner,
            trigger="interval",
            seconds=seconds,
            id=job_id,
            args=args
        )
        return job

    def modify_job(self, job_id=None, seconds=None):
        logger.info("Modify schedule job[%s]: interval [%d]" % (job_id, seconds))
        job = self.sdu.modify_job(
            job_id=job_id,
            seconds=seconds
        )
        return job

    def remove_job(self, job_id, fuzzy=False):
        if fuzzy is True:
            # not exactly job_id, such as ip
            jobs = self.get_jobs()
            for job in jobs:
                real_job_id = job.id
                if real_job_id.find(job_id) != -1:
                    logger.info("Start remove job id: %s" % real_job_id)
                    self.sdu.remove_job(real_job_id)
        else:
            logger.info("Start remove job id: %s" % job_id)
            if self.get_job(job_id):
                self.sdu.remove_job(job_id)
            else:
                logger.warning("Job id <%s> no found" % job_id)

    def print_jobs(self):
        self.sdu.print_jobs()

    def get_jobs(self):
        return self.sdu.get_jobs()

    def get_job(self, job_id):
        return self.sdu.get_job(job_id)

    def start(self):
        self.sdu.start()

    def stop(self):
        self.sdu.stop()

    def shutdown(self):
        self.sdu.shutdown()
