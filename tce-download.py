##############################################
#
# Tiny Core Linux *.tcz packages downloader
#
##############################################

# packages
import requests
from os import system as sh
from os import listdir
import sys

##############################################
#
#             DOWNLOAD ROUTINES
#
##############################################

# download file
def download(url, mode):
  filename = url.split('/')[-1]
  res = requests.get(url)
  if res.status_code != 200:
    if '.dep' in filename and res.status_code == 404: return 0
    else: print('filename: "' + filename + '"', res, 'doesn\'t exist!'); return 2
  else:
    print('Downloading "' + filename + '"... OK')
    with open(TCE_PATH + filename, mode) as f:
      f.write(res.text if mode == 'w' else res.content)
    return 1

# fetch package
def fetch(item):
  # substitute KERNEL
  if 'KERNEL' in item:
    item = item.replace('KERNEL', '5.15.10-tinycore64')
    # for 32-bit version use '5.15.10-tinycore'
  
  # init urls
  tcz = MIRROR + item
  md5 = tcz + '.md5.txt'
  dep = tcz + '.dep'
  
  # download package
  if download(tcz, 'wb') == 2: return
  
  # download checksum
  download(md5, 'w')
  
  # check checksums
  sh('md5sum ' + TCE_PATH + item + ' > ' + TCE_PATH + 'test.' + item)
  with open(TCE_PATH + 'test.' + item) as f: checksum = f.read().split(' ')[0]
  with open(TCE_PATH + item + '.md5.txt') as f: candidate = f.read().split(' ')[0]
  if checksum != candidate: print('Checksome... FAILED'); sys.exit(1)
  print('Checksum... OK')
  sh('rm -f ' + TCE_PATH + 'test.' + item)

  # resolve dependencies recursively
  if download(dep, 'w'):
    depfile = dep.split('/')[-1]
    with open(TCE_PATH + depfile) as f:
      items = f.read().split('\n')
      for dep_item in items[:-1] if len(items) > 1 else items:
        if dep_item != ' ':
          if dep_item in listdir(TCE_PATH): return 1
          print('Resolving dependency for "' + item + '":', dep_item)
          fetch(dep_item)

##############################################
#
#                  SETTINGS
#
##############################################

# mirror to download packages from
MIRROR = 'http://repo.tinycorelinux.net/13.x/x86_64/tcz/'

# tce package folder
TCE_PATH = './tce/optional/'

##############################################
#
#                     MAIN
#
##############################################

# clean up directory
sh('rm -rf tce')

# create directories
sh('mkdir tce && mkdir tce/optional')

# init downloads
with open('download.lst') as f: downloads = f.read().split('\n')[:-1]

# loop over the download items
for item in downloads:
  try:
    fetch(item)
    with open('./tce/onboot.lst', 'a') as f:
      f.write(item + '\n')
  except Exception as e: print(e)
