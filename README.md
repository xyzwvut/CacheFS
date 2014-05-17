CacheFS
=======
A FUSE file system that caches remote files.

Open -> lookup file -> fetch into cache -> local operations

'cfs synch' to push changes to the server

Run
===
python direct.py /Users/sb/cachefs/back/ /Users/sb/cachefs/front/


Run unit tests
==============
make test
Add -s to disable capturing (print() will be shown)

Design
======
/front    Contains the virtual view using cache and backend
/cache    Contains the medata
/back     Way to access the data on the server

Server
======
- Read config file
- Cache pools (pinned/LRU)
- Start FUSE driver

Fuse
====
- File operations
  - open
  - close
  - read
  - write

Cache
=====
Store the cached files somewhere locally.
Called from within the FUSE driver.
- open (bring in the file)
- read (look in cache)
- wirte (write through to server)
- close (v2 sync out)

Cache is organized in pools (LRU, pinned)?

Syncer
=======
Keep log of modified files.
Push them via the backend to the server if avialable.

Backend
=======
Abstract away different forms to access the files on the server
e.g. cp, rsync, SSHFS, SMB, AFP, ssh, ftp
- Interface
  - list files (pathname)
  - get  (pathname, offset, size)
  - push (pathname, offset, size)

Cmdline Tools
=============
- status, utilization
- pin files
- fetch files
- push/synch back to origin


-------------------------------------------------------------------------------
--
-- Implementation
--
-------------------------------------------------------------------------------

Class: Directory
----------------
- Root directory is mountpoint of front
- Contains list of Files

Class: File
-------------
- Cached?
- Location where stored in cache
- Location where stored in back
- Attributes, Size
- List of chunks

Class: Chunk
------------
- File, base
- offset, size
- dirty
- pool

Class: Cache
------------
- List of pools (pinned, LRU)
- Container for files
- Keep log of modified chunks
- Sync operation to flush changes to server

Class: Backend
--------------
Wrapps file operations to the server, supports multiple protocols
- ls-directory (pathname) ?
- ls-file (pathname) ?
- get  (pathname, offset, size)
- push (pathname, offset, size)

