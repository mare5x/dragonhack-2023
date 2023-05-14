from transformers import ViltProcessor, ViltForQuestionAnswering
from PIL import Image
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import torch

PROCESSOR = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
MODEL = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")


def vqa(image: Image, question: str, n=5) -> list:
    """ Returns a list of n best answers for the given image and question. """
    # prepare inputs
    encoding = PROCESSOR(image, question, return_tensors="pt")

    # forward pass
    outputs = MODEL(**encoding)
    logits = torch.softmax(outputs.logits, dim=1)
    # select n best answers
    n_best_idx = torch.topk(logits, n).indices[0].tolist()
    n_best_responses = [(MODEL.config.id2label[idx], logits[0][idx].item()) for idx in n_best_idx]
    return n_best_responses


def demo():
    """ Demo of the VQA MODEL_NAME, using the webcam images and question
    "What is the weather like?". """
    webcam_data = json.load(open("webcam_info.json"))

    for webcam_id, webcam in webcam_data.items():
        f_name = f"webcam_images/{webcam_id}.jpg"
        image = Image.open(f_name)
        text = "What is the weather like?"

        best_answers = vqa(image, text, n=3)

        title = f"In {webcam['location']} the weather is: " \
                f"\n-{best_answers[0][0]} with p={round(best_answers[0][1], 3)}" \
                f"\n-{best_answers[1][0]} with p={round(best_answers[1][1], 3)}" \
                f"\n-{best_answers[2][0]} with p={round(best_answers[2][1], 3)}"

        img = mpimg.imread(f_name)
        plt.imshow(img)
        plt.title(title)
        plt.plot()
        plt.show()


if __name__ == "__main__":
    # demo()

    print(vqa(Image.open("webcam_images/HRIBI-4323_.jpg"), "How many boats are there?"))
