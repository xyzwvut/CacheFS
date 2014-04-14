CacheFS
=======

A FUSE file system that caches remote files

Run
python direct.py /Users/sb/cachefs/back/ /Users/sb/cachefs/front/


Run unit tests
==============

CacheFS.git/tests$ py.test --front-dir=/Users/sb/cachefs/front/ -vv -x

Add -s to disable capturing (print() will be shown)

