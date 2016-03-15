#!/bin/bash

start() 
{
    service agent start $@
}

stop() 
{
    service agent stop
}

reload()
{
    service agent reload $@
}

status()
{
    service agent status
}

## Check to see if we are running as root first.
if [ "$(id -u)" != "0" ]; then
    echo "This script must be run as root" 1>&2
    exit 1
fi

case "$1" in
    start)
        start ${@:2}
        exit 0
    ;;
    stop)
        stop
        exit 0
    ;;
    restart)
        stop
        start  ${@:2}
        exit 0
    ;;
    reload)
	reload ${@:2}
	exit 0
    ;;
    status)
	status
	exit 0
    ;;
    **)
        echo "Usage: $0 {start|stop|restart|reload|status}" 1>&2
        exit 1
    ;;
esac
