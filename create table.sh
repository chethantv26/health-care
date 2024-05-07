#!/bin/bash

for f in *.csv; do 
	python "/home/`whoami`/health-care/mysql create table.py" "$f"
done