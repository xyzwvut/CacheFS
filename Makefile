
.PHONY: run test tests

run:
	PYTHONPATH=${PWD} ./server/main.py -c server/my_config.cfg

test_frontend:
	PYTHONPATH=${PWD} python3 server/frontend.py /Users/sb/cachefs/test/back /Users/sb/cachefs/test/front

test: tests

tests:
	py.test --front-dir=/Users/sb/cachefs/test/front/ -vv -s -x
