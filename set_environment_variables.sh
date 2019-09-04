#!/bin/bash

FILE=$1

if [ -z "$FILE" ]
then
    echo "Give file name as parameter!"
    return 0
fi

if [ ! -f "$FILE" ]
then
    echo "$FILE not exists"
    return 0
fi

cat "$FILE" | while read line; do
    echo $line
    export $line
done
