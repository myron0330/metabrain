#!/bin/bash
 
for i in $@
do
 if ! grep -qi Copyright $i
 then
 echo "adding licence file to:" $i
 cat LICENSE.txt $i >$i.new && mv $i.new $i
 fi
done
