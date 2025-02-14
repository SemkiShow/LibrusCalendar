#!/bin/bash
nano librus_key.txt
mkdir venv
python3 -m venv venv/
source venv/bin/activate
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib librus-apix
python3 get_token.py
sudo cp -r . /usr/local/bin/LibrusCalendar
cd /usr/local/bin/LibrusCalendar
source venv/bin/activate
sudo cp librus.service /etc/systemd/system
sudo systemctl daemon-reload
sudo systemctl enable librus.service
sudo systemctl start librus.service
systemctl status librus.service
