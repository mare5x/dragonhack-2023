import requests
import json
from PIL import Image
import os
from vqa import vqa
from prompt_creation import *
from geopy.distance import geodesic

MODEL_NAME = "gpt-3.5-turbo"
TOKEN = "VJ7c9CyPPsSgcJpbgWVfpUkG1s4jHN"


def get_response(prompt):
    """ returns a response for a given prompt """
    json_prompt = {
        "model": MODEL_NAME,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openai-api.meetings.bio/api/openai/chat/completions",
                             headers={"Authorization": f"Bearer {TOKEN}"}, json=json_prompt)
    return response


def parse_user_input(user_input):
    """ parses user input and returns the response from the model """
    prompt = parse_input(user_input)
    print(f"prompt: {prompt}")

    response = get_response(prompt)
    if response.ok:
        return json.loads(response.json()["choices"][0]["message"]["content"])
    return None


def image_id_to_location(image_id):
    """ return location for a given image_id """
    image_mapping = json.load(open("webcam_info.json"))
    return image_mapping[image_id]["location"]


def output_opinion_about_locations(location, response, question):
    """ returns models opinion about teh given location """
    print("output_opinion_about_locations", location)
    prompt = describe_location(location, response, question)
    print(prompt)

    response = get_response(prompt)
    if response.ok:
        return response.json()["choices"][0]["message"]["content"]
    return None


def vqa_image_id(image_id, query, n=1):
    """ returns best n responses as given by the visual question answering model
     for the given image and query """
    image = Image.open(f"webcam_images/{image_id}.jpg")
    response = vqa(image, query, n=n)
    return image, response


def get_image_by_location(task):
    """ returns the image, location and models response for the given task """
    print("get_photo_by_location", task)
    location = task.get("location")
    image_mapping = json.load(open("webcam_info.json"))

    image_id = None
    for key, value in image_mapping.items():
        if value["location"].lower() == location.lower():
            image_id = key
            break

    if image_id is not None:
        image = Image.open(f"webcam_images/{image_id}.jpg")
        print("I should count") if "count" in task.get("question") else 2
        response = vqa(image, task.get("question"), n=1 if "count" in task.get("question") else 2)
        return image, location, response
    return None, None, None


def get_relevant_photos_preferred_weather(task):
    print("get_relevant_photos", task)

    image_mapping = json.load(open("webcam_info.json"))
    preferred_weather = task["preferred_weather"]
    images = map(lambda x: x[:-4], os.listdir("webcam_images"))

    cached_prompts = json.load(open("cached_prompts.json"))
    result = []

    for image in images: 	
        if image + preferred_weather in cached_prompts:
            res = cached_prompts[image+preferred_weather]
        else:
            res = vqa(Image.open(f"webcam_images/{image}.jpg"), f"Is it {preferred_weather}?", n=1)
            cached_prompts[image+preferred_weather] = res

        if res[0][0].lower() == "yes":
            result.append((image, image_mapping[image]["location"], res[0][1]))

    with open("cached_prompts.json", "w") as outfile:
        json.dump(cached_prompts, outfile)
    return sorted(result, key=lambda x: x[2], reverse=True)


def get_distances_to_locations(coordinates):
    """ return a list of distances to locations """
    coordinates = [coordinates[1], coordinates[0]]
    image_mapping = json.load(open("webcam_info.json"))
    distances = []
    for key, value in image_mapping.items():
        distances.append((value["location"], geodesic(coordinates, value["coordinates"]).km))
    return sorted(distances, key=lambda x: x[1])


def get_location_opinion(task):
    """ get weather status at some fixed location specified in task """
    breakpoint()
    image, location, response = get_image_by_location(task)
    response = output_opinion_about_locations(location, response, task.get("question"))
    return dict(model_response=response, image=image, location=location)


def get_location_recommendation(task):
    """ returns recommendation of location based on users weather preferences specified in task """
    relevant_photos = get_relevant_photos_preferred_weather(task)
    if task.get("distance") is not None:
        distances = get_distances_to_locations(task.get("user_location"))
        good_locations = list(map(lambda x: x[0], filter(lambda x: x[1] < task.get("distance"),
                                                         distances)))
        relevant_photos = list(filter(lambda x: x[1] in good_locations, relevant_photos))

    image_id = relevant_photos[0][0]
    image = Image.open(f"webcam_images/{image_id}.jpg")
    model_prompt = describe_location_general(task, relevant_photos)
    response = get_response(model_prompt)
    if response.ok:
        model_response = response.json()["choices"][0]["message"]["content"]
        return dict(model_response=model_response, image=image,
                    location=image_id_to_location(image_id))
    return None


def ask_GPT(prompt):
    parsed_prompt = parse_user_input(prompt)
    print(f"{parsed_prompt=}")
    
    task_name = parsed_prompt.get("task")
    if task_name == "location_prediction":
        return task_name, get_location_opinion(parsed_prompt)
    elif task_name == "location_recommendation":
        return task_name, get_location_recommendation(parsed_prompt)
    elif task_name == "other":
        return task_name, parsed_prompt.get("answer")
    else:
        return None  # TODO


if __name__ == "__main__":
    test1 = {
        "task": "location_recommendation",
        "user_location": [46.0569, 14.5058],
        "preferred_weather": "sunny",
        "preferred_activity": "swimming"
    }
    
    print(ask_GPT("Where is it sunny?"))
    # print(parse_user_input("What is the weather like in Čmaribor?"))
    # print(get_location_recommendation(test1))
