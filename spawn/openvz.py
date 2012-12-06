# Primary interface to interacting with an OpenVZ container
# all operations run through here
import subprocess
import shlex

def sh(cmd):
  # execute a command and return stdout
  return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()[0]

class openvz():
  def __init__(self):
    pass

  def list(self):
    # return a list of the current containers
    vzlist_raw = sh('/usr/sbin/vzlist').splitlines()
    vzlist = {}
    for line in vzlist_raw:
      tokens = line.split()
      try:
        ctid = int(tokens[0])
        vzlist[ctid] = {}
      except ValueError:
        continue

      vzlist[ctid]['NPROC'] = tokens[1]
      vzlist[ctid]['STATUS'] = tokens[2]
      vzlist[ctid]['IP_ADDR'] = tokens[3]
      vzlist[ctid]['HOSTNAME'] = tokens[4]

    return vzlist

  def create(self, ctid, osname):
    # create a container
    return sh(shlex.split('/usr/sbin/vzctl create %s --ostemplate %s' % (ctid, osname)))

  def start(self,ctid):
    # start a container
    return sh(shlex.split('/usr/sbin/vzctl start %s' %(ctid)))

  def set(self, ctid, param, value):
    # set a value on the container
    return sh(shlex.split('/usr/sbin/vzctl set %s --%s %s --save' %(ctid, param, value)))

  def execute(self, ctid, command):
    # execute a command on the container
    return sh(shlex.split('/usr/sbin/vzctl exec %s %s' %(ctid, command)))
