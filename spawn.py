#!/usr/bin/env python
# The main script to bring in the module and execute ops against it
from optparse import OptionParser
import subprocess
import time
import sys
import os
sys.path.insert(0, '.')
from spawn import spawn

def opts():
  # Setup options for the script
  parser = OptionParser()
  parser.add_option("-f", "--file", dest="filename",help="file to serve", type="string", metavar="FILE")
  parser.add_option("-c", "--count", dest="count",help="servers to create", type="int", metavar="INTEGER")
  parser.add_option("-b", "--base-name", dest="basename",help="base of hostname", type="string", metavar="HOSTNAME")
  (options, args) = parser.parse_args()
  return options

def webcheck(path):
  # Curl a path, if the curl fails return false, otherwise return true
  try:
    subprocess.check_call(['/usr/bin/curl','-s',path], stderr=open('/dev/null', 'w'), stdout=open('/dev/null', 'w'))
    return True
  except subprocess.CalledProcessError:
    return False

if __name__=="__main__":
  options = opts()
  # All options are not options...
  if options.filename is None or options.count is None or options.basename is None:
    print "use --help for help, file, count, and basename must all be defined"
    sys.exit(1)

  sleeptime = 10

  for i in range(1,options.count+1):
    filename_nopath = os.path.basename(options.filename)
    container = spawn()
    print "INFO: Building Container: %s" %(options.basename + "-" + str(i))
    container.new(options.basename + "-" + str(i))
    webpath = "http://" + container.ip + "/" + filename_nopath
    print "INFO: Build Complete: %s created with IP %s and ID %s" %(options.basename + "-" + str(i), container.ip, container.ctid)
    print "INFO: Starting container, sleeping %s seconds" %(sleeptime)
    container.start()
    # This is a horrible hack, and rather than a waiting period, should do something to check and see if
    # the container is up and running 100%
    time.sleep(sleeptime)
    print "INFO: Putting files in place, updating host packages, and ensuring apache is present and running."
    container.file(options.filename,"/var/www/html/%s" %(filename_nopath))
    container.execute("/usr/bin/yum --assumeyes --quiet update")
    container.execute("/usr/bin/yum --assumeyes --quiet install http")
    container.execute("/sbin/service httpd start")
    container.execute("/sbin/chkconfig httpd on")
    webpath = "http://" + container.ip + "/" + filename_nopath
    if webcheck(webpath):
      print "INFO: Was able to retrieve %s" %(webpath)
    else:
      print "ERROR: Unable to retrieve %s" %(webpath)
