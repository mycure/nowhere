nowhere
=======

This script takes a path to a directory, walks through it, finds PDFs and
tries to compress them and, if successful, replaces them with the compressed
versions.

## Standalone

First, install the dependencies:
- Ghostscript
- Python packages: ghostscript and termcolor

You can run the script, passing the path to the directory containing the PDFs
you want to compress.

```
$> ./nowhere.py /path/to/something/
```

## Docker

You can also run the script within a Docker image which already contains its
dependencies:

```
$> docker run --rm -v /path/to/something/:/data nowhere:0.1 /data
```
