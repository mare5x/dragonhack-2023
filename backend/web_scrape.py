import json
import requests

LINK_PREFIX = "https://vreme.arso.gov.si"


def save_image(image_url, image_id):
    """ save image from url to disk
    :param image_url: url of image to save
    :param image_id: id of image to save (used as filename)"""
    try:
        img_data = requests.get(image_url).content
        with open(f'webcam_images/{image_id}.jpg', 'wb') as handler:
            handler.write(img_data)
    except Exception as e:
        print(f"Error saving image {image_id}: {e}")


def create_webcam_json():
    """ create json file with information about webcams as a dictionary where each webcam has the
    following structure:
    "webcam_id": {
        "location": location of the webcam,
        "coordinates": latitude and longitude of the webcam,
        "direction": direction of the webcam,
        "region": region of the webcam,
        "webcam_url": url to latest available image from the webcam
    } """
    webcam_list_url = LINK_PREFIX + "/api/1.0/webcam_list/"
    scraped_text = requests.get(webcam_list_url).text
    scraped_json = json.loads(scraped_text)
    webcam_list = scraped_json["webcam_list"]["features"]

    webcam_json = {}

    for webcam in webcam_list:
        direction = webcam["properties"]["directions"][0]
        location_id = webcam["properties"]["id"]

        # get link to the latest image from the webcam
        dict_key = f"webcam_{location_id}{direction}_data.json"
        camera = scraped_json.get(dict_key)
        webcam_url = None
        if camera is not None and len(camera) > 0:
            last_shot = camera[-1]
            webcam_url = LINK_PREFIX + last_shot["path"]

            webcam_json[location_id] = {
                "location": webcam["properties"]["title"],
                "coordinates": webcam["geometry"]["coordinates"],
                "direction": direction,
                "region": webcam["properties"]["parent_id"],
                "webcam_url": webcam_url
            }

    json.dump(webcam_json, open("webcam_info.json", "w"), indent=4, ensure_ascii=False)


def download_images():
    """ download images from webcams and save them to disk """
    webcam_info = json.load(open("webcam_info.json", "r"))
    for key, value in webcam_info.items():
        cam_url = value["webcam_url"]
        save_image(cam_url, key)


if __name__ == '__main__':
    create_webcam_json()
    download_images()
