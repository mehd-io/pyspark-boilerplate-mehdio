import pytest
from datajob.helpers.spark import get_spark_session
from pyspark.sql import SparkSession


@pytest.fixture(name="spark", scope="session")
def fixture_spark() -> SparkSession:
    return get_spark_session(app_name="test")
