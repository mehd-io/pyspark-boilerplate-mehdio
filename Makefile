PY_MODULES=datajob tests
RCFILE=setup.cfg

#----------- Tests -------------------------------------------------------------
test:
	@$(PRE_ACTIVATE) $(MAKE) -j4 --no-print-directory \
		test-unit \
		test-black \
		test-isort \
		test-pylint \
		test-mypy

test-black: # code formatter
	black -l 80 $(PY_MODULES)

test-mypy:  # typing check
	mypy $(PY_MODULES)

test-pylint:
	pylint -f parseable \
		--rcfile=${RCFILE} \
		-j 4 \
		$(PY_MODULES)

test-unit:
	pytest -vvv -rf -q --cov \
		--cov-report term \
		$(PY_MODULES) \
		$(PYTESTFLAGS)

test-isort:
	isort -l80 -m3 -c --tc $(PY_MODULES)

#----------- DEV ---------------------------------------------------------------

black: ## Format all the python code
	black -l 80 $(PY_MODULES)

isort: ## Sort imports in the python module
	isort -l80 -m3 --tc $(PY_MODULES)

#------------ PACKAGING  -------------------------------------------------------

package:
	./docker/script/package_zip.sh 

#------------ RUN/DEBUG  -------------------------------------------------------
run:
	/usr/spark-3.1.1/bin/spark-submit \
	--jars jars/spark-excel_2.11-0.9.9.jar \
	--py-files /workspaces/pyspark-boilerplate-mehdio/datajob.zip \
	--files /workspaces/pyspark-boilerplate-mehdio/configs/etl_config.json \
	datajob/cli.py \
	--job-name demo_job