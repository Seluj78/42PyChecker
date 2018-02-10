#!/bin/bash

RMVFUNCTIONS=$1

awk -v RMVFUNCTIONS="^[\t]?(#define)[\t ]*(${RMVFUNCTIONS})" '
BEGIN {
  RMV=0
}
$0 ~ RMVFUNCTIONS {
  RMV=1
}
{
  if (RMV == 0) {
    print $0
  } else {
    printf "//%s\n", $0;
    RMV++;
    if (RMV == 3) {
      RMV=0
    }
  }
}
' "Maintest/libft/main.c" 1>"libft_main.c" 2>".mymaintest"