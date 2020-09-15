import requests
import json

JWT_Key = ""


# Gets the unique user ID associated with the users email

def get_user_ID(email):
	base_url = "https://api.zoom.us/v2/users/{}".format(email)
	id_dictionary = {}
	id_dictionary["access_token"] = JWT_Key
	meeting_data = requests.get(base_url, params = id_dictionary)
	meeting_json = meeting_data.json()
	return meeting_json["id"]

#Gets the unique meeting ID for meetings within a monthly range(It can only search monthly). Adding in input functionality later for user input. Right now this only extracts the ID from the first entry for testing purposes
def get_meeting_ID(ID):
	base_url = "https://api.zoom.us/v2/users/{}/recordings".format(ID)
	id_dictionary = {}
	id_dictionary["access_token"] = JWT_Key
	id_dictionary['from'] = "2020-03-01"
	id_dictionary['to'] = "2020-03-30"
	meeting_data = requests.get(base_url, params = id_dictionary)
	meeting_json = meeting_data.json()
	print(meeting_json["meetings"][0]["recording_files"][0]["meeting_id"])
	return meeting_json

#Downloads the meeting as a python object

def download_meeting(meetingID):
	base_url = "https://api.zoom.us/v2/meetings/{}/recordings".format(meetingID)
	id_dictionary = {}
	id_dictionary["access_token"] = JWT_Key
	download_file = requests.get(base_url, params = id_dictionary)
	make_json = download_file.json()
	call_download_url = make_json["recording_files"][0]["download_url"]
	download_url = "https://api.zoom.us/v2/meetings/{}/recordings/".format(meetingID)
	get_recording = requests.get(call_download_url, params = id_dictionary)
	return get_recording.content

#Saves the meeting locally to the machine for now. Eventually I'll probably just erase this and pass the object right to vimeo as a byte object if its possible. 

def save_meeting(meeting):
	with open("zoom.mp4", "wb") as f:
		f.write(download_meeting(meeting))