import requests
import json
from PIL import Image
import os
from vqa import vqa



#prompt = "Write a haiku about DragonHack."
model = "gpt-3.5-turbo"
#token = "rehvDn6zukf53UQG9W0xZ4WRTsmDV4"
token = "VJ7c9CyPPsSgcJpbgWVfpUkG1s4jHN"

def getResponse(prompt):

	response = requests.post(
	"https://openai-api.meetings.bio/api/openai/chat/completions",
	headers={"Authorization": f"Bearer {token}"},
	json={
	# specification of all options: https://platform.openai.com/docs/api-reference/chat/create
	"model": model,
	"messages": [{"role": "user", "content": prompt}],
	},
	)
	return response


def parseUserInput(user_text):
	prompt = f"""
	You will be given a user prompt delimited by <<< and >>>.

	Extract from user prompt to what location is the user refering.

	Generate a question that is like users, but without the specified location.

	For example:
	input: What is the weather like in london?
	your output: What is the weather?
	input: Is it cloudy or foggy in london?
	your output: Is it cloudy or is it foggy?



	You need to construct a JSON.
	Use the following format:
	location: <user refering location - string>
	question: <generated question - string>

	Output JSON: <json with location and question>


	<<<{user_text}>>>
	"""
	response = getResponse(prompt)
	if getResponse(prompt).ok:
		print(response.json()["choices"][0]["message"]["content"])
		return response.json()["choices"][0]["message"]["content"]
	return None

def outputOpinionAboutLocations(locations):
	###generate format
	chat_txt = ""
	for loc in locations:
		loc_txt = str(loc[1])+"-"
		for fact in loc[2]:
			loc_txt += fact[0]+","
		loc_txt = loc_txt[:-1]+";"
		chat_txt += loc_txt
	print(chat_txt)
	prompt = f"""
	You will be provided with text delimited by < and >.
	Text will be of format location-fact,...,fact;location-fact,...fact;...
	facts are based on the location

	Generate text for each location, describe it based on facts about it.

	<{chat_txt}>
	"""
	response = getResponse(prompt)
	if getResponse(prompt).ok:
		print(response.json()["choices"][0]["message"]["content"])
		return response
	return None





def getRelevantPhotos(task):
	location = task.get("location")
	print(location)
	image_mapping = json.load(open("webcam_info.json"))

	images = []
	for key,value in image_mapping.items():
		if value["location"].lower() == location.lower():
			images.append(key)
	#print(image_mapping)
	#images = os.listdir("webcam_images")
	#images = map(lambda x: x.split(".")[0],images)
	#print(list(images))
	#images = list(filter(lambda x: image_mapping[x]["location"].lower() == location.lower(),images))
	
	result = []
	for image in images: 		#########zaenkrat ignorirajmo loop
		## prepare inputs
		res = vqa(Image.open(f"webcam_images/{image}.jpg"),task.get("question"))
		result.append((image,location,res))
	
	return result

def askGPT(prompt):

	prompt = "What is the weather like in koper?"
	#input_parse = parseUserInput(prompt)
	#task = json.loads(input_parse)
	task = json.loads("""{
	"location": "koper",
	"question": "What is the weather like?"
	}""")
	relPhotos = getRelevantPhotos(task)
	response = outputOpinionAboutLocations(relPhotos)

	print(response)

	return response
	