#! /usr/bin/env python3

import os
import sys
import json
import hashlib
import tempfile
from termcolor import colored

def hash(path):
  hasher = hashlib.sha1()
  with open(path, 'rb') as fd:
    buffer = fd.read()
    hasher.update(buffer)
  return hasher.hexdigest()

if len(sys.argv) != 2:
  print("[usage] %s {path to the directory containing PDFs to compress}")
  sys.exit(1)

path_target = sys.argv[1]
path_log = path_target + '/.log'

if os.path.isfile(path_log):
  with open(path_log, 'r') as fd:
    log = json.load(fd)
else:
  log = []
  with open(path_log, 'w') as fd:
    json.dump(log, fd)

path_nowhere = path_target + '/.nowhere/'

if not os.path.exists(path_nowhere):
  os.makedirs(path_nowhere)

for directory, subdirectories, files in os.walk(path_target):
  for file in files:
    if not file.endswith('.pdf'):
      continue
    path_input = directory + '/' + file
    checksum_input = hash(path_input)
    if not checksum_input in log:
      fd, path_output = tempfile.mkstemp(dir = path_nowhere)
      os.close(fd)
      rv = os.system('ps2pdf -dPDFSETTINGS=/ebook "%s" "%s"' % (path_input, path_output))
      if rv != 0:
        print('[%s]    %s' % (colored('ERROR', 'red'), path_input))
        os.remove(path_output)
        continue
      checksum_output = hash(path_output)
      size_input = os.path.getsize(path_input)
      size_output = os.path.getsize(path_output)
      if size_output < size_input:
        print('[%s] %s (%s) %s > %s (%.3f%%)' % (colored('COMPRESS', 'green'), path_input, checksum_output, size_input, size_output, size_output / size_input))
        os.rename(path_output, path_input)
      else:
        print('[%s]  %s (%s) %s < %s' % (colored('IGNORED', 'blue'), path_input, checksum_output, size_input, size_output))
        os.remove(path_output)
      log += [checksum_output]
      with open(path_log, 'w') as fd:
        json.dump(log, fd)
    else:
      print('[%s]     %s (%s)' % (colored('SKIP', 'yellow'), path_input, checksum_input))
