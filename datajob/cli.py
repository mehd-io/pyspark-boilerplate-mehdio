import typer
import importlib
import time
import datetime
from loguru import logger

app = typer.Typer()


@app.command()
def run(job_name: str = typer.Option("")) -> None:
    """Run given job name"""
    start = time.time()
    try:
        module = importlib.import_module(f"jobs.{job_name}")
        module.run()
        end = time.time()
        logger.info(f"Execution of job {job_name} took {end - start} seconds")
    except Exception as e:
        logger.info(
            str(datetime.datetime.now())
            + "____________ Abruptly Exited________________"
        )
        raise Exception(f"Exception::Job {job_name} failed with msg {e}")


if __name__ == "__main__":
    app()
