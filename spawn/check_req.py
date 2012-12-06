# Provide and centralize requirements checking
import subprocess
import os.path

def sh(cmd):
  # execute a command and return stdout
  return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

def check_req():
  # Ensure the host meets requirements
  if not os.path.isfile('/etc/redhat-release'):
  	return False
  if not os.path.isfile('/usr/sbin/vzctl'):
  	return False
  if not os.path.exists('/vz'):
  	return False
  return True