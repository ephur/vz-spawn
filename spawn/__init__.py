# The main coordinator of the system
import sys
import shutil
from spawn.ip import get_ip
from spawn.id import get_id
from spawn.check_req import check_req
from spawn.openvz import openvz


class spawn():

  def __init__(self):
    # Check system requirements, and hard fail if they aren't met
    if not check_req():
      print "ERROR: System does not meet requirements"
      # @TODO implement Exception types, and raise instead of exit
      sys.exit(1)
    self.ovz = openvz()

  def new(self, hostname, ctid=None, ip=None, nameserver='8.8.8.8', osname="centos-6-x86_64"):
    if ip == None:
      ip = get_ip()
    if ctid == None:
      ctid = get_id()

    self.ctid = ctid
    self.ip = ip
    self.osname = osname
    self.nameserver = nameserver
    self.hostname = hostname

    self.ovz.create(self.ctid, self.osname)
    self.ovz.set(self.ctid, 'ipadd', self.ip)
    self.ovz.set(self.ctid, 'nameserver', self.nameserver)
    self.ovz.set(self.ctid, 'hostname', self.hostname)
    return self.ctid

  def start(self):
    self.ovz.start(self.ctid)

  def execute(self,cmd):
    self.ovz.execute(self.ctid,cmd)

  def file(self,source,dest):
    shutil.copyfile(source,"/vz/private/%s%s" %(self.ctid, dest))