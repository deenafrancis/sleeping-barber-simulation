#!/bin/bash




/usr/bin/python sim.py &

pid1=$!

/usr/bin/python -m SimpleHTTPServer 8998 &> /dev/null &

pid2=$!

echo "In the browser go to the url 'http://localhost:8998/sim.html'"

echo "Press ctrl+c to quit"

trap "kill -9 $pid1 $pid2 $$" SIGINT SIGTERM

while [ 1 -gt 0 ]
do
    echo -n "."
    sleep 1
done
