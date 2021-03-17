"""
Simple Demo pipeline logic
"""
from pyspark.sql.functions import col, concat_ws, lit
from datajob.helpers.spark import get_spark_session
from loguru import logger
from datajob.configs import etl_config
from pyspark.sql import DataFrame, SparkSession, Row

def run(job_name: str) -> None:
    """Main ETL script definition.
    """
    config = getattr(etl_config, job_name)
    spark = get_spark_session(app_name=job_name)

    logger.info("Creating test data for ETL")
    df = create_test_data(spark)

    logger.info("Doing some data transformation")
    df_tf = transform_data(df, config["job_parameter"]["demo_job"]["steps_per_floor"])

    logger.info("Dumping dataset...")
    dump_data(df_tf, config["paths"]["output_data_demo_job"])
    logger.info("dataset dumped on: " + config["paths"]["output_data_demo_job"])


def transform_data(df:DataFrame, steps_per_floor:int)-> DataFrame:
    """Transform original dataset.
    """
    df_transformed = df.select(
        col("id"),
        concat_ws(" ", col("first_name"), col("second_name")).alias("name"),
        (col("floor") * lit(steps_per_floor)).alias("steps_to_desk"),
    )

    return df_transformed


def dump_data(df:DataFrame, path:str)-> None:
    """Collect data locally and write to CSV.
    """
    df.write.csv(path, mode="overwrite", header=True)


def create_test_data(spark:SparkSession)-> DataFrame:
    """Create test data.
    This function creates both both pre- and post- transformation data
    saved as Parquet files in tests/test_data. This will be used for
    unit tests as well as to load as part of the example ETL job.
    """
    # create example data from scratch
    local_records = [
        Row(id=1, first_name="Dan", second_name="Germain", floor=1),
        Row(id=2, first_name="Dan", second_name="Sommerville", floor=1),
        Row(id=3, first_name="Alex", second_name="Ioannides", floor=2),
        Row(id=4, first_name="Ken", second_name="Lai", floor=2),
        Row(id=5, first_name="Stu", second_name="White", floor=3),
        Row(id=6, first_name="Mark", second_name="Sweeting", floor=3),
        Row(id=7, first_name="Phil", second_name="Bird", floor=4),
        Row(id=8, first_name="Kim", second_name="Suter", floor=4),
    ]

    return spark.createDataFrame(local_records)


def get_df_from_excel(spark, file_path, sheet_name):
    """
    This method is intended to create a dataframe form excel file
    """
    return (
        spark.read.format("com.crealytics.spark.excel")
        .option("useHeader", "true")
        .option("treatEmptyValuesAsNulls", "true")
        .option("inferSchema", "true")
        .option("addColorColumns", "False")
        .option("maxRowsInMey", 2000)
        .option(sheet_name, "Import")
        .load(file_path)
    )
