#!/bin/sh

_N=$((2 * 1024 * 1024))

for i in 2 4 8 16
do
	python skydata.py $_N $i c
	python skydata.py $_N $i i
	python skydata.py $_N $i a
done
