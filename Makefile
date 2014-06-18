
.PHONY: run test tests

BASEDIR=/Users/sb/cachefs/test
FRONTDIR=${BASEDIR}/front
BACKDIR=${BASEDIR}/back

run:
	PYTHONPATH=${PWD} ./server/main.py -c server/my_config.cfg

testfileops:
	${eval MY_TEMPDIR = ${shell mktemp -d /tmp/test_cachefs_XXXXX}}
	py.test --front-dir=${MY_TEMPDIR} -vv -s -x
	rm -rf ${MY_TEMPDIR}

testfrontend:
	PYTHONPATH=${PWD} python3 server/frontend.py ${BACKDIR} ${FRONTDIR}

test: tests
tests:
	py.test --front-dir=${FRONTDIR} -vv -s -x
