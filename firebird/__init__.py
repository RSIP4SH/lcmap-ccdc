from pyspark import SparkConf
from pyspark import SparkContext
import datetime
import logging
import os
import socket
import sys

HOST = socket.gethostbyname(socket.getfqdn())

AARDVARK = os.getenv('AARDVARK', 'http://localhost:5678')
AARDVARK_SPECS = os.getenv('AARDVARK_SPECS', '/v1/landsat/chip-specs')
AARDVARK_CHIPS = os.getenv('AARDVARK_CHIPS', '/v1/landsat/chips')
CHIPS_URL = ''.join([AARDVARK, AARDVARK_CHIPS])
SPECS_URL = ''.join([AARDVARK, AARDVARK_SPECS])

CASSANDRA_CONTACT_POINTS = os.getenv('CASSANDRA_CONTACT_POINTS', '0.0.0.0')
CASSANDRA_USER = os.getenv('CASSANDRA_USER')
CASSANDRA_PASS = os.getenv('CASSANDRA_PASS')
CASSANDRA_KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'lcmap_changes_local')
CASSANDRA_RESULTS_TABLE = os.getenv('CASSANDRA_RESULTS_TABLE', 'results')
CASSANDRA_JOBCONF_TABLE = os.getenv('CASSANDRA_JOBCONF_TABLE', 'jobconf')

INITIAL_PARTITION_COUNT = os.getenv('INITIAL_PARTITION_COUNT')
PRODUCT_PARTITION_COUNT = os.getenv('PRODUCT_PARTITION_COUNT')
STORAGE_PARTITION_COUNT = os.getenv('STORAGE_PARTITION_COUNT')

DRIVER_HOST = os.getenv('DRIVER_HOST', HOST)

LOG_LEVEL = os.getenv('FIREBIRD_LOG_LEVEL', 'INFO')

SPARK_MASTER = os.getenv('SPARK_MASTER', 'spark://localhost:7077')
SPARK_EXECUTOR_IMAGE = os.getenv('SPARK_EXECUTOR_IMAGE')
SPARK_EXECUTOR_CORES = os.getenv('SPARK_EXECUTOR_CORES', 1)
SPARK_EXECUTOR_FORCE_PULL = os.getenv('SPARK_EXECUTOR_FORCE_PULL', 'false')

QA_BIT_PACKED = os.getenv('CCD_QA_BITPACKED', 'True')

logging.basicConfig(
    stream=sys.stdout,
    level=LOG_LEVEL,
    format='%(asctime)s %(module)s::%(funcName)-20s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# default all loggers to WARNING then explictly override below
logging.getLogger("").setLevel(logging.WARNING)

# let firebird.* modules use configuration value
logger = logging.getLogger('firebird')
logger.setLevel(LOG_LEVEL)


def sparkcontext():
    try:
        ts = datetime.datetime.now().isoformat()
        conf = (SparkConf().setAppName("lcmap-firebird-{}".format(ts))
                .setMaster(SPARK_MASTER)
                .set("spark.mesos.executor.docker.image", SPARK_EXECUTOR_IMAGE)
                .set("spark.executor.cores", SPARK_EXECUTOR_CORES)
                .set("spark.mesos.executor.docker.forcePullImage",
                     SPARK_EXECUTOR_FORCE_PULL))
        return SparkContext(conf=conf)
    except Exception as e:
        logger.info("Exception creating SparkContext: {}".format(e))
        raise e


def ccd_params():
    params = {}
    if QA_BIT_PACKED is not 'True':
        params = {'QA_BITPACKED': False,
                  'QA_FILL': 255,
                  'QA_CLEAR': 0,
                  'QA_WATER': 1,
                  'QA_SHADOW': 2,
                  'QA_SNOW': 3,
                  'QA_CLOUD': 4}
    return params


def available_products():
    '''
    Products that can be requested from firebird.
    :return: Set of available products
    '''
    jobconf = {'chip_ids': None,
               'initial_partitions': None,
               'specs_url': None,
               'specs_fn': None,
               'chips_url': None,
               'chips_fn': None,
               'acquired': None,
               'chip_spec_queries': None,
               'clip_box': None,
               'product_partitions': None}
    sc = None
    try:
        sc = pyspark.SparkContext()
        return set(firebird.rdds.products(jobconf, sc).keys())
    finally:
        if sc is not None:
            sc.stop()


def evaluate(acquired, bounds, clip, directory, product, product_dates):
    pass


def save(acquired, bounds, clip, product, product_dates):
    pass


def count(bounds, product):
    pass


def missing(bounds, product):
    pass


def errors(bounds, product):
    pass
