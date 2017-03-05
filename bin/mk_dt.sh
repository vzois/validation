#!/bin/sh

_N=$((16 * 1024 * 1024))

for i in 8
do
	python skydata.py $_N $i c
	python skydata.py $_N $i i
	python skydata.py $_N $i a
done
