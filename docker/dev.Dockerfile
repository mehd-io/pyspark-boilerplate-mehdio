FROM docker.io/library/openjdk:11.0.10-slim

# Debian 10 has py 3.7 by default
RUN apt-get update && apt-get install -y git zip unzip software-properties-common curl python3-pip && apt-get clean

# Py
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
RUN python3 -m pip install --upgrade pip

#######################################
# HADOOP AND SPARK
#######################################

# SPARK 
ENV SPARK_VERSION 3.1.1
ENV HADOOP_VERSION 3.2
ENV SPARK_PACKAGE spark-${SPARK_VERSION}-bin-hadoop${HADOOP_VERSION}
ENV SPARK_HOME /usr/spark-${SPARK_VERSION}
ENV PATH $PATH:${SPARK_HOME}/bin
RUN curl -sL --retry 3 \
  "https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/${SPARK_PACKAGE}.tgz" \
  | gunzip \
  | tar x -C /usr/ \
  && mv /usr/$SPARK_PACKAGE $SPARK_HOME \
  && chown -R root:root $SPARK_HOME

ENV PYSPARK_DRIVER_PYTHON python3
ENV PYSPARK_PYTHON python3
# Point to py4j deps
ENV PYTHONPATH ${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-0.10.9-src.zip:$PYTHONPATH

CMD ["bash"]