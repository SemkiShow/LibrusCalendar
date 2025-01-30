# Init
import json, datetime, time, os.path
from librus_apix.schedule import get_schedule, schedule_detail

def GetSchedule(month, year):
  output = []
  try:
    schedule = get_schedule(client, month, year)
    for day in schedule:
      for event in schedule[day]:
        prefix, href = event.href.split('/')
        details = schedule_detail(client, prefix, href)
        output.append(details)
    print("Loaded " + str(month) + "-" + str(year))
  except Exception:
    print("Failed to load " + str(month) + "-" + str(year))
  try:
    schedule = get_schedule(client, str(int(month)+1), year)
    for day in schedule:
      for event in schedule[day]:
        prefix, href = event.href.split('/')
        details = schedule_detail(client, prefix, href)
        output.append(details)
    print("Loaded " + str(int(month)+1) + "-" + str(year))
  except Exception:
    print("Failed to load " + str(int(month)+1) + "-" + str(year))
  return output

def AddEvent(summary, description, date):
  event = {
    'summary': summary,
    'description': description,
    'start': {
        'date': date,
        'timeZone': 'Europe/Warsaw',
    },
    'end': {
        'date': date,
        'timeZone': 'Europe/Warsaw',
    },
  }
  event = service.events().insert(calendarId='primary', body=event).execute()
  print('Event created: %s' % (event.get('htmlLink')))

def GetCalendar(month, year):
  page_token = None
  now = year + "-" + month + "-01T00:00:00.000000Z"
  events_result = (
      service.events().list(
          calendarId="primary",
          timeMin=now,
          singleEvents=True,
          orderBy="startTime",
      )
      .execute()
  )
  events = events_result.get("items", [])
  return events

# Setup Librus
from librus_apix.client import Client, Token, new_client

librusFile = open("librus_key.txt", "r")
librusKey = librusFile.read()
client: Client = new_client()
_token: Token = client.get_token(librusKey.split(",")[0], librusKey.split(",")[1])
librusFile.close()

# Setup Google
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]

creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists("token.json"):
  creds = Credentials.from_authorized_user_file("token.json")
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
  if creds and creds.expired and creds.refresh_token:
    creds.refresh(Request())
  else:
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
  # Save the credentials for the next run
  with open("token.json", "w") as token:
    token.write(creds.to_json())

service = build("calendar", "v3", credentials=creds)

# Main loop
while True:
  print("Getting the calendar...")
  currentDate = str(datetime.datetime.now()).split(" ")[0].split("-")
  events = GetCalendar(currentDate[1], currentDate[0])

  print("Getting the Librus schedule...")
  schedule_dir = GetSchedule(currentDate[1], currentDate[0])
  schedule_list = []
  for schoolEvent in schedule_dir:
    schedule_list.append(list(str(schoolEvent)))
  schedule = []
  for schoolEvent in schedule_list:
    for i in range(len(schoolEvent)):
      if schoolEvent[i] == "'":
        schoolEvent[i] = "\""
    schedule.append("".join(schoolEvent))
    # print("".join(schoolEvent))

  print("Comparing the results...")
  foundInCalendar = False
  for schoolEvent in schedule:
    for calendarEvent in events:
      if "Opis" in json.loads(schoolEvent):
        if calendarEvent["summary"] == json.loads(schoolEvent)["Opis"]:
          foundInCalendar = True
      else:
        foundInCalendar = True
    if foundInCalendar == False:
      print(json.loads(schoolEvent))
      AddEvent(json.loads(schoolEvent)["Opis"], json.loads(schoolEvent)["Przedmiot"], json.loads(schoolEvent)["Data"])
      print("Added " + json.loads(schoolEvent)["Opis"])
    foundInCalendar = False

  print("Waiting...")
  time.sleep(60*60)
