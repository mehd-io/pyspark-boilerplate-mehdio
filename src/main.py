import importlib
import argparse
import time
import datetime
import click # Not used, for the sake of the boilerplate to check external package deps

if __name__ == '__main__':
    project_name = '_____________________PYSPARK-BOILERPLATE_____________________'
    parser = argparse.ArgumentParser(description=project_name)
    parser.add_argument('--job','-j', type=str, required=True, dest='job_name', help="The name of the job module you want to run. (ex: dataPrepartion.dataIngestion will run dataIngestion.py job of dataPrepartion package)")
    args = parser.parse_args()
    print (project_name)
    print("Executing with following arguments\n %s" %args)
    start = time.time()
    try:
        module = importlib.import_module(args.job_name)
        module.main()
        end = time.time()
        print ("\nExecution of job %s took %s seconds" % (args.job_name, end-start))
    except Exception as e:
         print (str(datetime.datetime.now()) + "____________ Abruptly Exited________________")
         raise Exception("Exception::Job %s failed with msg %s" %(args.job_name, str(e)))



