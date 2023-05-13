import requests
import json
from PIL import Image
import os
from vqa import vqa
from prompt_creation import *

# prompt = "Write a haiku about DragonHack."
model = "gpt-3.5-turbo"
# token = "rehvDn6zukf53UQG9W0xZ4WRTsmDV4"
token = "VJ7c9CyPPsSgcJpbgWVfpUkG1s4jHN"


def get_response(prompt):
    # specification of all options: https://platform.openai.com/docs/api-reference/chat/create
    json_prompt = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openai-api.meetings.bio/api/openai/chat/completions",
                             headers={"Authorization": f"Bearer {token}"}, json=json_prompt)
    return response


def parse_user_input(user_text):
    prompt = parse_input(user_text)

    response = get_response(prompt)
    if get_response(prompt).ok:
        return json.loads(response.json()["choices"][0]["message"]["content"])
    return None


def output_opinion_about_locations(location, response):
    print("output_opinion_about_locations", location)
    prompt = describe_location(location, response)
    print(prompt)

    response = get_response(prompt)
    if get_response(prompt).ok:
        # print(response.json()["choices"][0]["message"]["content"])
        return response.json()["choices"][0]["message"]["content"]
    return None


def get_relevant_photos(task):
    print("get_relevant_photos", task)
    location = task.get("location")
    image_mapping = json.load(open("webcam_info.json"))

    image_id = None
    for key, value in image_mapping.items():
        if value["location"].lower() == location.lower():
            image_id = key

    if image_id is not None:
        image = Image.open(f"webcam_images/{image_id}.jpg")
        response = vqa(image, task.get("question"), n=2)
        return image, location, response
    return None, None, None


def ask_GPT(prompt):
    parsed_prompt = parse_user_input(prompt)
    image, location, response = get_relevant_photos(parsed_prompt)
    response = output_opinion_about_locations(location, response)

    return response, image


if __name__ == "__main__":
    ask_GPT("What is the weather like in Ljubljana?")
