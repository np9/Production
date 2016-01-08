#!/bin/sh
pip install -r requirements.txt
python suppression.py
python creation.py
python insertions.py
python run.py
