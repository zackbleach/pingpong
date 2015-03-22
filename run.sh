if [ -z ${PINGPONG_PORT+x} ]; 
    then 
        gunicorn app:app -b localhost:6000;
    else 
        gunicorn app:app -b localhost:$PINGPONG_PORT
fi

