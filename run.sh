#!/bin/sh
if [ -z ${PINGPONG_PORT+x} ]; 
    then 
        gunicorn app:app -b localhost:6000 --pid /tmp/pingpong.pid
    else 
        gunicorn app:app -b localhost:$PINGPONG_PORT --pid /tmp/pingpong.pid
fi

