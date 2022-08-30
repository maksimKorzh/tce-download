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

# mirror to download packages from
MIRROR = 'http://repo.tinycorelinux.net/13.x/x86_64/tcz/'

# tce package folder
TCE_PATH = './tce/optional/'

# clean up directory
sh('rm -rf tce')

# create directories
sh('mkdir tce && mkdir tce/optional')

# init downloads
with open('download.lst') as f: downloads = f.read().split('\n')[:-1]

# download file
def download(name, mode):
  filename = name.split('/')[-1]
  res = requests.get(name)
  if res.status_code != 200:
    if '.dep' in name and res.status_code == 404: return 0
    else: print(res, 'FAILED'); sys.exit(1)
  else:
    print('Downloading "' + filename + '"... OK')
    with open(TCE_PATH + filename, mode) as f:
      f.write(res.text if mode == 'w' else res.content)
    return 1

# fetch package
def fetch(item):
  tcz = MIRROR + item
  md5 = tcz + '.md5.txt'
  dep = tcz + '.dep'
  
  # download files
  download(tcz, 'wb')
  download(md5, 'w')

  # resolve dependencies recursively
  if download(dep, 'w'):
    depfile = [i for i in listdir(TCE_PATH) if (item + '.dep') in i][0]
    with open(TCE_PATH + depfile) as f:
      for dep_item in f.read().split('\n')[:-1]:
        fetch(dep_item)

# loop over the download items
for item in downloads:
  fetch(item)
  with open('./tce/onboot.lst', 'a') as f:
    f.write(item)
