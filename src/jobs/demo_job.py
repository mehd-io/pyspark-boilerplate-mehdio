from pyspark.sql import Row
from pyspark.sql.functions import col, concat_ws, lit
import sys
from src.helpers.spark import start_spark

def main():
    """Main ETL script definition.
    :return: None
    """
    # start Spark application and get Spark session, logger and config
    spark, log, config = start_spark(
        app_name='my_etl_job')
    
    # log that main ETL job is starting
    log.warn('etl_job is up-and-running')

    # execute ETL pipeline
    log.warn('Creating test data for ETL')
    df = create_test_data(spark)
    log.warn('Doing some data transformation')
    df_tf = transform_data(df, config['job_parameter']['demo_job']['steps_per_floor'])
    log.warn('Final Dataset')
    print(df_tf.show())
    dump_data(df_tf, config['paths']['output_data_demo_job'])
    log.warn('dataset dumped on: '+config['paths']['output_data_demo_job'])
    # log the success and terminate Spark application
    log.warn('test_etl_job is finished')

def transform_data(df, steps_per_floor):
    """Transform original dataset.
    :param df: Input DataFrame.
    :param steps_per_floor_: The number of steps per-floor at 43 Tanner
        Street.
    :return: Transformed DataFrame.
    """
    df_transformed = (
        df
        .select(
            col('id'),
            concat_ws(
                ' ',
                col('first_name'),
                col('second_name')).alias('name'),
               (col('floor') * lit(steps_per_floor)).alias('steps_to_desk')))

    return df_transformed


def dump_data(df,path):
    """Collect data locally and write to CSV.
    :param df: DataFrame to print.
    :return: None
    """
    (df.write
       .csv(path, mode='overwrite', header=True))
    return None


def create_test_data(spark):
    """Create test data.
    This function creates both both pre- and post- transformation data
    saved as Parquet files in tests/test_data. This will be used for
    unit tests as well as to load as part of the example ETL job.
    :return: df
    """
    # create example data from scratch
    local_records = [
        Row(id=1, first_name='Dan', second_name='Germain', floor=1),
        Row(id=2, first_name='Dan', second_name='Sommerville', floor=1),
        Row(id=3, first_name='Alex', second_name='Ioannides', floor=2),
        Row(id=4, first_name='Ken', second_name='Lai', floor=2),
        Row(id=5, first_name='Stu', second_name='White', floor=3),
        Row(id=6, first_name='Mark', second_name='Sweeting', floor=3),
        Row(id=7, first_name='Phil', second_name='Bird', floor=4),
        Row(id=8, first_name='Kim', second_name='Suter', floor=4)
    ]

    df = spark.createDataFrame(local_records)

    return df

def get_df_from_excel(spark, file_path, sheet_name):
    """
    This method is intended to create a dataframe form excel file
    :param spark: spark Session
    :param file_path:  hdfs path of the file
    :return: dataframe
    """
    return (spark.read.format("com.crealytics.spark.excel")
                        .option("useHeader", "true")
                        .option("treatEmptyValuesAsNulls", "true")
                        .option("inferSchema", "true")
                        .option("addColorColumns", "False")
                        .option("maxRowsInMey", 2000)
                        .option(sheet_name, "Import")
                        .load(file_path))


# entry point for PySpark ETL application
if __name__ == '__main__':
    sys.exit(main())
