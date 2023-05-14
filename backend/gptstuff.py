import requests
import json
from PIL import Image
import os
from vqa import vqa
from prompt_creation import *
from geopy.distance import geodesic

# prompt = "Write a haiku about DragonHack."
model = "gpt-3.5-turbo"
# token = "rehvDn6zukf53UQG9W0xZ4WRTsmDV4"
token = "VJ7c9CyPPsSgcJpbgWVfpUkG1s4jHN"




def get_response(prompt):
    # specification of all options: https://platform.openai.com/docs/api-reference/chat/create
    json_prompt = {
        "model": model,
        "temperature": 0,
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post("https://openai-api.meetings.bio/api/openai/chat/completions",
                             headers={"Authorization": f"Bearer {token}"}, json=json_prompt)
    return response


def parse_user_input(user_text):
    prompt = parse_input(user_text)
    print(f"{prompt=}")

    response = get_response(prompt)
    if response.ok:
        return json.loads(response.json()["choices"][0]["message"]["content"])
    return None

def image_id_to_location(image_id):
    image_mapping = json.load(open("webcam_info.json"))
    return image_mapping[image_id]["location"]


def output_opinion_about_locations(location, response, question):
    print("output_opinion_about_locations", location)
    prompt = describe_location(location, response,question)
    print(prompt)

    response = get_response(prompt)
    if response.ok:
        # print(response.json()["choices"][0]["message"]["content"])
        return response.json()["choices"][0]["message"]["content"]
    return None

def vqa_image_id(image_id, query, n=1):
    image = Image.open(f"webcam_images/{image_id}.jpg")
    response = vqa(image, query, n=n)
    return image, response

def get_relevant_photos(task):
    print("get_relevant_photos", task)
    location = task.get("location")
    image_mapping = json.load(open("webcam_info.json"))

    image_id = None
    for key, value in image_mapping.items():
        if value["location"].lower() == location.lower():
            image_id = key
            break

    if image_id is not None:
        image = Image.open(f"webcam_images/{image_id}.jpg")
        print("I should count") if "count" in task.get("question")  else 2
        response = vqa(image,task.get("question"), n=1 if "count" in task.get("question")  else 2)
        return image, location, response
    return None, None, None

def get_relevant_photos_preffered_weather(task):
    print("get_relevant_photos", task)

    image_mapping = json.load(open("webcam_info.json"))
    preffered_weather = task["prefered_weather"]
    images = map(lambda x: x[:-4],os.listdir("webcam_images")) #remove .jpg

    cached_prompts = json.load(open("cached_prompts.json"))
    result = []
    for image in images: 	
        ## prepare inputs
        if image+preffered_weather in cached_prompts:
            res = cached_prompts[image+preffered_weather]
            print("cached!")
        else:
            res = vqa(Image.open(f"webcam_images/{image}.jpg"),"Is it "+preffered_weather+"?",n=1)
            cached_prompts[image+preffered_weather] = res
        print(res)
        
        if res[0][0].lower() == "yes":
            result.append((image,image_mapping[image]["location"],res[0][1]))

    with open("cached_prompts.json", "w") as outfile:
        json.dump(cached_prompts, outfile)
    return sorted(result,key=lambda x: x[2],reverse=True)

def get_distances_to_locations(loc):
    loc = [loc[1],loc[0]]
    image_mapping = json.load(open("webcam_info.json"))
    distances = []
    for key,value in image_mapping.items():
        print(loc)
        print(value['coordinates'])
        distances.append((value["location"],geodesic(loc,value["coordinates"]).km))
    return sorted(distances,key=lambda x: x[1])

#fuction preforming task of getting weather status at some fixed location
def get_location_opinion(task):
    image, location, response = get_relevant_photos(task)	#get relevant camera images		
    response = output_opinion_about_locations(location, response,task.get("question"))	#generate response based on images
    return dict(model_response=response, image=image, location=location)

#user asked for recommendation of location based on his weather preferences
def get_location_recommendation(task):
    relPhotos = get_relevant_photos_preffered_weather(task)	#get relevant camera images
    #did user specify distance?
    if task.get("distance") != None:
        distances = get_distances_to_locations(task.get("user_location"))
        ok_lokacije = list(map(lambda x: x[0],filter(lambda x: x[1] < task.get("distance"),distances)))
        relPhotos = list(filter(lambda x: x[1] in ok_lokacije,relPhotos))

    image_id = relPhotos[0][0]
    image = Image.open(f"webcam_images/{image_id}.jpg")
    model_prompt = describe_location_general(task, relPhotos)
    response = get_response(model_prompt)
    if response.ok:
        model_response = response.json()["choices"][0]["message"]["content"]
    return dict(model_response=model_response, image=image, location=image_id_to_location(image_id))

def ask_GPT(prompt):
    parsed_prompt = parse_user_input(prompt)
    print(f"{parsed_prompt=}")
    
    task_name = parsed_prompt.get("task")
    if task_name == "location_prediction":
        return task_name, get_location_opinion(parsed_prompt)
    elif task_name == "location_recommendation":
        return task_name, get_location_recommendation(parsed_prompt)
    elif task_name == "nonvalid":
        return task_name, parsed_prompt.get("answer")
    else:
        return None  # TODO

if __name__ == "__main__":
    test1 ={ 
            "task": "location_recommendation",
            "user_location": [46.0569, 14.5058],
            #"distance": 120,
            "prefered_weather": "sunny",
            "prefered_activity": "swimming"
        }
    
    print(ask_GPT("Where is it sunny?"))
    #print(parse_user_input("What is the weather like in Čmaribor?"))
    #print(get_location_recommendation(test1))
