import pytest
from pyspark.sql import SparkSession
from datajob.helpers.spark import get_spark_session


@pytest.fixture(name="spark", scope="session")
def fixture_spark() -> SparkSession:
    return get_spark_session(app_name="test")
