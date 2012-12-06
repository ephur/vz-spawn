# A class to give an IP address to a container
# Manages a repository of IP addresses and returns available
# It's simple right now, has a predefined range,
# and checks against VZlist, however more robust provisioning systems
# need to have an easy external hook to get IP's from a web service
import spawn.openvz
from random import choice

def get_ip():
  pool = []
  [pool.append('192.168.0.' + str(x)) for x in range(255) if x > 100]
  o = spawn.openvz()
  container_list = o.list()

  for container in container_list:
    try:
    	pool.remove(container_list[container]['IP_ADDR'])
    except ValueError:
    	pass

  return choice(pool)