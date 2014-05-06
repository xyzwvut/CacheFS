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
- Local to local backend
3. Design
- How does the FUSE interface look?
- What is the smallest tool that works?
- synch to push changes to server
- How to handle file cration?
- How to run it as a server?
- How to hook in a cmdline tool?
4. Prototype
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

