"""
Test the transform logics with sample of data
"""
from datajob.helpers.spark import get_spark_session
from datajob.jobs.demo_job import transform_data
from pyspark.sql import SparkSession
from pyspark.sql.functions import mean


def test_transform_data(spark: SparkSession, test_data_path="tests/fixtures/"):
    """Test data transformer.
    Using small chunks of input data and expected output data, we
    test the transformation step to make sure it's working as
    expected.
    """
    input_data = spark.read.parquet(test_data_path + "employees")

    expected_data = spark.read.parquet(test_data_path + "employees_report")

    expected_cols = len(expected_data.columns)
    expected_rows = expected_data.count()
    expected_avg_steps = expected_data.agg(
        mean("steps_to_desk").alias("avg_steps_to_desk")
    ).collect()[0]["avg_steps_to_desk"]

    data_transformed = transform_data(input_data, 21)

    cols = len(expected_data.columns)
    rows = expected_data.count()
    avg_steps = expected_data.agg(
        mean("steps_to_desk").alias("avg_steps_to_desk")
    ).collect()[0]["avg_steps_to_desk"]

    assert expected_cols == cols
    assert expected_rows == rows
    assert expected_avg_steps == avg_steps
    assert [
        col in expected_data.columns for col in data_transformed.columns
    ] == [
        True,
        True,
        True,
    ]
