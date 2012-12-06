#!/bin/sh

# Define some constants
VZ_CTL='/usr/sbin/vzctl'
VZ_HOME='/vz'
VZ_BASE_NET='192.168.0'
VZ_TEMPLATE='centos-6-x86_64'
VZ_DOMAIN='ephur.net'

CURL='/usr/bin/curl'

# Check the path and ctl
[ -f ${VZ_CTL} ] || {
  echo "$0: ${VZ_CTL} not found, can't continue"
  exit 1
}

# Check the args
[ $# -eq 3 ] || {
  echo "$0: Usage:$0 <basename> <count> <file to serve>"
  exit 1
}

`echo $2 | grep -Eq '^[0-9]+$'` || {
  echo "Error: Count is not an integer"
  exit 1
}

[ -r $3 ] || {
  echo "Error: Can't read or find the file you want to serve."
  exit 1
}
BASENAME=$1
COUNT=$2
FILE=$3
FILE_BASE=${FILE##*/}

# Spin some stuff up
i=0
while [ $i -lt $2 ]; do
  i=`expr $i + 1`
  echo "Creating server #$i ${BASENAME}-$i.${VZ_DOMAIN} with IP ${VZ_BASE_NET}.$i, this may take some time"
  ${VZ_CTL} create $i --ostemplate ${VZ_TEMPLATE} > /dev/null || echo "ERROR: Creating container"
  ${VZ_CTL} set $i --ipadd ${VZ_BASE_NET}.$i --save > /dev/null
  ${VZ_CTL} set $i --nameserver 8.8.8.8 --save > /dev/null
  ${VZ_CTL} set $i --hostname ${BASENAME}-$i.${VZ_DOMAIN} --save > /dev/null
  echo "Starting server #$i"
  ${VZ_CTL} start $i > /dev/null 2>&1 || echo "ERROR: Starting server $i"
  sleep 5
  echo "Updating all packages and installing apache"
  ${VZ_CTL} exec $i '/usr/bin/yum --assumeyes --quiet update' > /dev/null 2>&1
  ${VZ_CTL} exec $i '/usr/bin/yum --quiet install httpd' > /dev/null 2>&1
  ${VZ_CTL} exec $i '/sbin/chkconfig httpd on' > /dev/null 2>&1
  ${VZ_CTL} exec $i '/sbin/service httpd start' > /dev/null 2>&1
  cp ${FILE} /vz/private/$i/var/www/html/ || echo "ERROR: Could not put ${FILE} in place to be served"
  ### When not waiting a moment, sometimes the curl returns before the container is ready to serve the file
  echo -n "Testing HTML return: http://${VZ_BASE_NET}.$i/${FILE_BASE}.... "
  {
    ${CURL} -sIk http://${VZ_BASE_NET}.$i/${FILE_BASE} > /dev/null && echo "SUCCESS";
  } || {
    echo "ERROR (failed to get 200 when requesting file)";
  }
done
