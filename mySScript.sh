#!/bin/bash
# chkconfig: 2345 80 80
# This will begin my python code, I hope :)

start() {
     python /usr/CRT_Comms/PowerLED.py
     python /usr/CRT_Comms/shutdown.py
}

stop() {
     pkill -f PowerLED.py
     pkill -f shutdown.py
     python /usr/CRT_Comms/LowerLED.py
     pkill -f LowerLED.py
}

case "$1" in
     start)
      start
      ;;
     stop)
      stop
      ;;
     restart)
      stop
      start
      ;;
     status)
      ;;
     *)
      echo "Usage: $0 {start|stop|status|restart}"
esac

exit 0

