# PySpark Boilerplate Mehdio :fire:

# Introduction

Running a prod-ready pyspark app can be difficult for many reasons :
- managing python packages w/ external jars
- Running in client mode vs cluster mode (logging and configiration management have different behaviours)

This boilerplate solves those problems by providing :

* Proper Folder structure for ETL applications
* Logging, configuration, spark session helpers packaged in a launch mode abstraction.
* Tests example (with data!)
* Helpers functions for packaging your application and spark-submit command examples

This project is initially a fork from : https://github.com/AlexIoannides/pyspark-example-project

Requirements :
* Pipenv
* Yarn (when running your job in cluster mode)

## Folder Structure

```
├── Pipfile
├── Pipfile.lock
├── README.md
├── configs // Job configuration
│   └── etl_config.json
├── jars // For spark java dependencies (here, lib to read excel file)
│   └── spark-excel_2.11-0.9.9.jar
├── setup.py // custom scripts to packages pythons dependencies
├── src // All the source code
│   ├── __init__.py
│   ├── helpers
│   │   ├── __init__.py
│   │   ├── logging.py
│   │   └── spark.py
│   ├── jobs
│   │   ├── __init__.py
│   │   └── demo_job.py
│   └── main.py
└── tests // All tests with sample data
    ├── __init__.py
    ├── test_data
    │   ├── employees
    │   │   ├── _SUCCESS
    │   │   └── part-00000-9abf32a3-db43-42e1-9639-363ef11c0d1c-c000.snappy.parquet
    │   └── employees_report
    │       ├── _SUCCESS
    │       └── part-00000-4a609ba3-0404-48bb-bb22-2fec3e2f1e68-c000.snappy.parquet
    └── test_etl_job.py
```

# How to use logging, configuration and spark helper
Depending on if you launch your spark-job in client or cluster mode, the way that logging and configuration are handled is a bit different.
The good news is that everyting is handled in src/helpers/spark.py and it will detect the launch mode at run time and according that, it will initiate the proper configuration/logging object.
The configuration instantiated will be available as a dict.

## Logging and Spark Session
```
from src.helpers.spark import start_spark

# Start Spark application and get Spark session, logger and config dict
spark, logger, config = start_spark(app_name='my_etl_job',conf_file=conf_file)

# Use logger
logger.warn('This is a warn message!')
logger.info('This is a info message!')
logger.error('This is a error message!')
```

## Configuration
A `JSON` Configuration file is passed when running the spark-submit command, there's a example in configs/etl_config.json
e.g :
```
 {
    "paths": {
        "sample_data":"/my/path/tmp/xls/sample_data.xls",
        "population":"/my/other_path/population.xls"
    }
}
```

Then once the config dict is instancied via the command above, you can use :
```
print(config['paths']['sample_data'])
# will print "/my/path/tmp/xls/sample_data.xls"
```

# How to write and run tests

In order to test with Spark, we use the `pyspark` Python package, which is bundled with the Spark JARs required to programmatically start-up and tear-down a local Spark instance.
Using `pyspark` to run Spark is an alternative way of developing with Spark as opposed to using the PySpark shell or `spark-submit`.

To run from end-to-end the data pipeline the test locally or in an CI/CD pipeline, we need a spark session. As we run locally, we need to initiate a spark session with *.master("local[*]")* parameter.
The trick here is to add a global env flag *["PYTEST"] = "1"* in the test script so that the spark.py handle the correct spark session to initiate.

There's an example of a full test in tests/test_etl_job.py.

Make sure you've installed the dev dependencies (pyspark) to run the test via :
```
pipenv install --dev
```
Then run test :
```
pipenv run pytest -q tests/test_etl_job.py
```

# How to package my application and run a spark-submit job
## Packaging your source code and python dependencies
You need the following files/zip : 
* source code (as .zip)
* python dependencies (as .zip)
* your external jars if your cluster is not connected to the internet(see in this boilerplate with spark-excel lib to be able to read excel files with spark) or
* File entry point :  main.py

Assuming that you used pipenv to manage your python dependencies, you can use a custom function in setup.py "bdist_spark" to have everything ready as a final .zip file (that you can store in an repository or deploy to a cluster).

All you have to do so is fill the PACKAGE_NAME and version in the setup.py and then :
```
python setup.py bdist_spark
```
and a ****_spark_dist.zip will be available.

## Writing your first data pipeline
The differents jobs (data pipeline) will be put under *src/jobs/my_job.py*
All jobs are considered as module, so that you can launch a specific job directly from the spark-submit command with the "-j" argument.

E.g, we have "demo_job" module in src/jobs/demo_job.py

spark-submit [...] src/main.py -j src.jobs.demo_job

## Launching your spark job

```
PYSPARK_PYTHON=/binaries/anaconda3/bin/python3 \ 
spark2-submit \
--deploy-mode client \ 
--jars jars/spark-excel_2.11-0.9.9.jar \ 
--py-files pyspark_boilerplate_mehdio-0.1.zip,pyspark_boilerplate_mehdio-0.1-deps.zip \  
--files /my/local/path/to/etl_config.json \
main.py \
-j src.jobs.demo_job
```

`PYSPARK_PYTHON` : Sometimes needed to specify python kernel if you have multiple

`--deploy-mode` : client or cluster mode

`--jars` : Your local jar dependencies, if you are connected to the internet, use --package com.maven.path to directly pull from maven for example. In this boilerplate, is to show the use of a lib to read excel file in spark, see in demo.job.py.

`--py-files`: python libs, python source code

`--files`: Configuration file pyspark_boilerplate_mehdio_0.1/main.py # File entry point

`main.py`: the entry point file.

`-j`:  Job name, which is a module.

# Extra notes
The spark.py file is handling the different spark session for a YARN cluster. If you work on K8s or mesos, you will need to tweak a bit the code.

# Extra ressources
https://github.com/AlexIoannides/pyspark-example-project
https://developerzen.com/best-practices-writing-production-grade-pyspark-jobs-cb688ac4d20f
https://stackoverflow.com/questions/47227406/pipenv-vs-setup-py
https://pipenv.readthedocs.io/en/latest/advanced/#pipfile-vs-setup-py
https://realpython.com/pipenv-guide/