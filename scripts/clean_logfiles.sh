#!/bin/bash

function check_cleanlog
  {
    local RET0 LOGFILENAME
    LOGFILENAME="$1"
    if [ -f "$LOGFILENAME" ]
    then
      RET0=`cat -e "$LOGFILENAME" | awk '{gsub(/\^M.*\^M/, ""); gsub(/\^@/, ""); gsub(/\^[\[]*[0-9;]*[MmHJ]/, "");  gsub(/[\$]$/, ""); print}'`
      echo "$RET0" > "$LOGFILENAME"
    fi
}

check_cleanlog $1