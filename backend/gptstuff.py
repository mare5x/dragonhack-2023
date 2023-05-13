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


#if getResponse(prompt).ok:
#   print(response.json()["choices"][0]["message"]["content"])


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
		return response
	return None


task = json.loads("""{
    "location": "koper",
    "question": "Is it raining or is it sunny?"
}""")

from transformers import ViltProcessor, ViltForQuestionAnswering
processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

def getRelevantPhotos(task):
	location = task.get("location")
	
	image_mapping = json.load(open("webcam_info.json"))
	#print(image_mapping)
	images = os.listdir("webcam_images")
	images = map(lambda x: x.split(".")[0],images)
	#print(list(images))
	images = list(filter(lambda x: image_mapping[x]["location"].lower() == location.lower(),images))
	print(images)
	for image in images:
		## prepare inputs
		encoding = processor(Image.open(f"webcam_images/{image}.jpg"),task.get("question"), return_tensors="pt")
		outputs = model(**encoding)
		logits = outputs.logits
		idx = logits.argmax(-1).item()
		print("Predicted answer:", model.config.id2label[idx])
		idx = logits.argmax(-2).item()
		print("Predicted answer:", model.config.id2label[idx])
		idx = logits.argmax(-3).item()
		print("Predicted answer:", model.config.id2label[idx])

getRelevantPhotos(task)