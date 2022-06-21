#!/bin/bash
source ~/.bash_profile
export PYTHONPATH=`pwd`

APP_PATH=`pwd`
type=$2

print_help()
{
    echo "Usage: "
    echo "    run.sh start|fstop"
    echo "    run.sh start (for background running)"
    echo "    run.sh fstop (exit)"
}

if [ $# -ne 1 ]
then
    print_help
    exit -1
fi


case "$1" in
    start)
        echo `pwd`
        echo "starting ..."
        nohup python $APP_PATH/run_http_scanner.py > nohup.out 2>&1 &
        if [ $? -ne 0 ]; then
            echo "fail to start easy_http_scanner"
            exit 255
        fi
        echo "starting finished..."
        exit 0
    ;;

    fstop)
        pid=`ps x | grep $APP_PATH/run_http_scanner.py | grep -v grep | awk '{print $1}'`
        if [ x"$pid" == x"" ]; then
            echo "no valid pid"
            break
        fi
        kill $pid
        echo "stop finished..."
        exit 0 
    ;;

    *)
        print_help
    ;;

esac
