#!/bin/bash

if [ ! -f bin/activate ];then
    python3 - m env .
if

source bin/activate
pip3 install -r requirements.txt
pyinstaller app.py
