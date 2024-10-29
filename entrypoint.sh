#!/bin/bash

X :0 -config dummy.conf &
sleep 20
python3  converter.py
