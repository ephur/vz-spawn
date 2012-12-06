# The ID might need to be mapped to something specific, so making this easy
# to replace with a funciton that returns or gets CTID's a different way
# should a more robust implementation be needed
import spawn.openvz
import os
from random import choice

def get_id():
  # Create a pool of ID's, and assign an ID from the pool
  pool = []
  [pool.append(int(x)) for x in range(1024) if x > 0]
  o = spawn.openvz()
  container_list = o.list()

  # Remove ID's of running containers
  for container in container_list:
    try:
    	pool.remove(container)
    except ValueError:
    	pass

  # Remove ID's that apper in /vz/private
  listing = os.listdir("/vz/private")
  for filename in listing:
    try:
      pool.remove(filename)
    except ValueError:
      pass

  return choice(pool)