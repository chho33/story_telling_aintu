#!/bin/bash

pip install -r requirements.txt
cd django-audiofield; python setup.py install
sudo apt -y install libsox-fmt-mp3 libsox-fmt-all mpg321 dir2ogg libav-tools sox
python manage.py makemigrations app
python manage.py migrate
