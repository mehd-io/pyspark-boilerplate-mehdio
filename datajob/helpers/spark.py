"""
Spark helpers
"""
from pyspark.sql import SparkSession

from loguru import logger

def get_spark_session(app_name:str
) -> SparkSession:
    """
    Create or get a spark session
    :param spark_session_option:
    :return: A spark session
    """
    logger.info("Getting the Spark Session.")
    return (
        SparkSession.builder.appName(app_name)
        .getOrCreate()
    )


