
.PHONY: test tests

run:
	PYTHONPATH=${PWD} ./server/main.py -c server/my_config.cfg

test: tests

tests:
	py.test --front-dir=/Users/sb/cachefs/test/front/ -vv -s -x
