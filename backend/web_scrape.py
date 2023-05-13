import json
import requests

LINK_PREFIX = "https://vreme.arso.gov.si"


def save_image(image_url, image_id):
    try:
        img_data = requests.get(image_url).content
        with open(f'webcam_images/{image_id}.jpg', 'wb') as handler:
            handler.write(img_data)
    except Exception as e:
        print(f"Error saving image {image_id}: {e}")


def create_webcam_json():
    webcam_list_url = "https://vreme.arso.gov.si/api/1.0/webcam_list/"
    text = requests.get(webcam_list_url).text
    webcam_info = json.loads(text)
    webcam_list = webcam_info["webcam_list"]["features"]

    webcam_json = {}

    for wl in webcam_list:
        location = wl["properties"]["title"]
        coordinates = wl["geometry"]["coordinates"]
        direction = wl["properties"]["directions"][0]
        location_id = wl["properties"]["id"]
        region = wl["properties"]["parent_id"]


        key = f"webcam_{location_id}{direction}_data.json"
        camera = webcam_info.get(key)

        cam_url = None
        if camera is not None and len(camera) > 0:
            last_shot = camera[-1]
            cam_url = LINK_PREFIX + last_shot["path"]

        webcam_json[location_id] = {
            "location": location,
            "coordinates": coordinates,
            "direction": direction,
            "region": region,
            "cam_url": cam_url
        }

    json.dump(webcam_json, open("webcam_info.json", "w"), indent=4, ensure_ascii=False)


def download_images():
    webcam_info = json.load(open("webcam_info.json", "r"))
    for key, value in webcam_info.items():
        cam_url = value["cam_url"]
        save_image(cam_url, key)


if __name__ == '__main__':
    # create_webcam_json()
    download_images()
