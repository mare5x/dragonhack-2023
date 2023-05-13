import requests
import json
from PIL import Image
import os
from vqa import vqa

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
    response = get_response(prompt)
    if get_response(prompt).ok:
        return json.loads(response.json()["choices"][0]["message"]["content"])
    return None


def output_opinion_about_locations(location):
    print("output_opinion_about_locations", location)
    # generate format
    chat_txt = ""

    loc_txt = str(location[1])+"-"
    for fact in location[2]:
        loc_txt += fact[0]+","
    loc_txt = loc_txt[:-1]+";"
    chat_txt += loc_txt
    print(chat_txt)
    prompt = f"""

    You will be provided with text delimited by < and >.
    Text will be of format location-fact,...,fact;location-fact,...fact;...
    facts are based on the location at this moment.

    Generate text for each location, describe it based on facts about it in this moment. 
    Be short and do no overexaggerate in your answers.

    <{chat_txt}>
    """
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
    response = output_opinion_about_locations((image, location, response))

    return response, image


if __name__ == "__main__":
    ask_GPT("What is the weather like in Ljubljana?")
