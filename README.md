# PySpark Boilerplate Mehdio :fire:

# Introduction

Running a prod-ready pyspark app can be difficult for many reasons : packaging, handling extra jars, easy local testing.

This boilerplate solves those problems by providing :

* Proper Folder structure for ETL applications
* Logging, configuration, spark session helpers
* Tests example (with data!)
* Helpers functions for packaging your application and spark-submit command examples
* A dev docker image (to be used with VS code or through the `make` docker commands) for a smooth local development.

This project is initially a fork from : https://github.com/AlexIoannides/pyspark-example-project

Requirements :
* Docker
* make
* Any Cloud Service that can run pyspark (AWS Glue, AWS EMR, GCP DataProc...)

## Development
### Build the dev image
```
make build-docker
```
### Run the tests
```
make test-docker
```
### Run the spark job demo_job
```
make run-docker
```
## Folder Structure

```
├── LICENCE
├── Makefile
├── README.md
├── datajob
│   ├── cli.py // Entry point of the spark job
│   ├── configs // hold static config of the etl
│   ├── helpers 
│   └── jobs // main logic
├── docker // for dev container
├── jars // extra jars (for reading from excel file)
├── poetry.lock
├── pyproject.toml
├── setup.cfg
├── setup.py
└── tests // test with fixtures data
```

## Configuration
Static configuration can be done through `./datajob/configs/etl_config.py`
The job name is provided at run time through `--job-name` (here `demo_job` as value).
For instance : 
```
	spark-submit \
	--jars jars/spark-excel_2.11-0.9.9.jar \
	--py-files datajob.zip \
	datajob/cli.py \
	--job-name demo_job
```
will run the job `datajob/jobs/demo_job.py` and the associated config value from `./datajob/configs/etl_config.py`.

# How to package my application and run a spark-submit job
## Packaging your source code and python dependencies
You need the following files/zip : 
* python dependencies that include your spark code(as .zip)
* your external jars if your cluster is not connected to the internet(see in this boilerplate with spark-excel lib to be able to read excel files with spark) or
* File entry point :  cli.py (located in `datajob/cli.py`)

To run a ready depencies folder as `.zip` run : 
```
make package
```
will generate a `datajob.zip`

## Writing your first data pipeline
The differents jobs (data pipeline) will be put under *datajob/jobs/my_job.py*
All jobs are considered as module, so that you can launch a specific job directly from the spark-submit command with the "--job-name" argument.

E.g, we have "demo_job" module in datajob/jobs/demo_job.py

spark-submit [...] datajob/cli.py --job-name demo_job

## Launching your spark job

```
	spark-submit \
	--jars jars/spark-excel_2.11-0.9.9.jar \
	--py-files datajob.zip \
	datajob/cli.py \
	--job-name demo_job
```

`--jars` : Your local jar dependencies, if you are connected to the internet, use --package com.maven.path to directly pull from maven for example. In this boilerplate, is to show the use of a lib to read excel file in spark, see in demo.job.py.

`--py-files`: python libs, python source code

`datajob/cli.py`: the entry point file.

`--job-name`:  custom job parameter Job name, which is a module.
# Extra ressources
https://github.com/AlexIoannides/pyspark-example-project
https://developerzen.com/best-practices-writing-production-grade-pyspark-jobs-cb688ac4d20f
https://stackoverflow.com/questions/47227406/pipenv-vs-setup-py
https://pipenv.readthedocs.io/en/latest/advanced/#pipfile-vs-setup-py
https://realpython.com/pipenv-guide/

 