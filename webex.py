""" Copyright (c) 2020 Cisco and/or its affiliates.
This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at
           https://developer.cisco.com/docs/licenses
All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. 
"""

from webexteamssdk import WebexTeamsAPI
from dotenv import load_dotenv
import os

# load all environment variables
load_dotenv()

api = WebexTeamsAPI(access_token=os.getenv("WEBEX_TEAMS_ACCESS_TOKEN"))

# Find all rooms that have 'webexteamssdk Demo' in their title
all_rooms = api.rooms.list()
demo_rooms = [room for room in all_rooms if 'webexteamssdk Demo' in room.title]

# Delete all of the demo rooms
for room in demo_rooms:
    api.rooms.delete(room.id)

# Create a new demo room
demo_room = api.rooms.create('webexteamssdk Demo')

# Add people to the new demo room
email_addresses = ["jbanegas@cisco.com"]
for email in email_addresses:
    api.memberships.create(demo_room.id, personEmail=email)

# Post a message to the new room, and upload a file
api.messages.create(demo_room.id, text="Welcome to the room!",
                    files=["https://www.webex.com/content/dam/wbx/us/images/dg-integ/teams_icon.png"])