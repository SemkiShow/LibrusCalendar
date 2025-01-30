# Librus Calendar
An application for automatically adding upcoming tests from Librus to Google Calendar

# Linux installation
- **Step 0** Install Python 3.10.7 or greater and pip

Note: if steps 1-4 aren't clear, you can [follow the official tutorial](https://developers.google.com/calendar/api/quickstart/python), stopping on installing pip packages
- **Step 1** [Create a Google Cloud project](https://console.cloud.google.com/projectcreate)
- **Step 2** [Enable the Google Calendar API](https://console.cloud.google.com/flows/enableapi?apiid=calendar-json.googleapis.com)
- **Step 3** [Configure OAuth](https://console.cloud.google.com/apis/credentials/consent)
- **Step 4** [Download credentials.json from your OAuth client](https://console.cloud.google.com/apis/credentials)
- **Step 5** Run these commands. A text editor will open. Enter your Librus username, followed by a comma, followed by your Librus password, all **without** any spaces (For example, username,password). After that, press Ctrl+S, then Ctrl+X. Let the script finish. If everything went correctly, you will see librus.service successfully running.
```bash
chmod +x install.sh
sudo ./install.sh
sudo systemctl status librus.service
```
