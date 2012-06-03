#!/bin/bash

# activate the virtualenv
# from outside 
#. $HOME/REST/bin/activate

# detach the REST server 
# save the pid to file descriptor 3
( python rgis.py & echo $! >&3 ) 3>pid

# leave sufficient time for the REST server to launch
sleep 2

#echo $(<pid)

# run the tests
curl http://localhost:5000/

curl http://localhost:5000/ls

#curl http://localhost:5000/ls/bin

curl http://localhost:5000/netAccumulate

curl http://lily.ccny.cuny.edu/rgis/netAccumulate

curl http://localhost:5000/elev/4.025/11.0802

curl http://localhost:5000/Africa/Elevation/15sec/4.025/11.0802

curl http://localhost:5000/Africa/Niger/Upstream/4.025/11.0802/5


# kill the server process
kill $(<pid)
