#!/bin/bash
cp -r .. /usr/local/bin
cd /usr/local/bin/LibrusCalendar
nano librus_key.txt
mkdir venv
python3 -m venv venv/
source venv/bin/activate
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib librus-apix
cp librus.service /etc/systemd/system
systemctl daemon-reload
systemctl enable librus.service
systemctl start librus.service
sudo systemctl status librus.service
