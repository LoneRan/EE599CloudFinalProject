#!/bin/bash
sudo apt-get update
sudo apt-get -y install python3-pip
sudo apt install virtualenv
virtualenv env
source env/bin/activate

sudo pip3 install flask-sqlalchemy

export FLASK_APP=app.py
pip3 install fuzzywuzzy
pip3 install mysql-connector
pip3 install statsmodels 
flask run --host=0.0.0.0
