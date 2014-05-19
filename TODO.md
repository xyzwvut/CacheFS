TODOs:
1. [OK] Null FS
2. Tests
- [OK] Use python
- [OK] Create file
- Delete file
- [OK] Set permissions
- [OK] Write file
- [OK] Read file
- [OK] Copy file
- Cleanup leftover files
- Integrate server tests
- [ok] Rsync list file
- [ok] Rsync list directory
- [ok] Rsync file size
- Rsync files permissions
- Understand overall hierarchy
- Go my iTunes files and inspect their atributes
3. Design
- Request -> Look in cache -> pass on to backend
- What happens if backend is disconnected and IO comes in?
- How does the FUSE interface look?
- What is the smallest tool that works?
- synch to push changes to server
- How to handle file cration?
- [ok] How to run it as a server?
- [ok] How to hook in a cmdline tool?
4. Prototype
- Where to put the humanfriendly module?
- Keep track of current size of the cache
- Print size of the cache
- [ok] How to pass cache, backend around?
- Local to local backend
- CTRL+c should gracefully shut down cmd and then the server
- Open file
- Fetch file into cache
- Read/write into the cache
- Write back to origin
5. CacheFS driver frontend
6. CacheFS driver backend
7. Library that keeps track what is there
8. Library that fetches from server
- Chunks are files
9. Library for chunks of 64 KB
- How to store meta-data?
- Put meta-data for file-parts into database?
10. Small files loaded from local to local?
11. How to sych between remote and local?
12. Fetched from remote machine
13. Use cliff for console and argparse integration?

https://code.google.com/p/pyfilesystem/
https://github.com/terencehonles/fusepy

Wrapper for FUSE

# Yes.
http://osxfuse.github.io/

# Not?
brew install fuse4x fuse4x-kext

