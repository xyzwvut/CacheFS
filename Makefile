
.PHONY: run test tests

BASEDIR=/Users/sb/cachefs/test
FRONTDIR=${BASEDIR}/front
BACKDIR=${BASEDIR}/back

run:
	PYTHONPATH=${PWD} ./server/main.py -c server/my_config.cfg

test_frontend:
	PYTHONPATH=${PWD} python3 server/frontend.py ${BACKDIR} ${FRONTDIR}

test: tests

tests:
	py.test --front-dir=${FRONTDIR} -vv -s -x
