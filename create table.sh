#!/bin/bash

for f in *.csv; do 
	python3 "./mysql create table.py" "$f"
done
