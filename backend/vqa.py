from transformers import ViltProcessor, ViltForQuestionAnswering
import requests
from PIL import Image


def vqa(image: Image, question: str) -> str:
    pass

# prepare image + question
# url = "http://images.cocodataset.org/val2017/000000039769.jpg"
url = "https://meteo.arso.gov.si//uploads/probase/www/observ/webcam/LJUBL-ANA_BEZIGRAD_dir/siwc_20230513-1100_LJUBL-ANA_BEZIGRAD_nw.jpg"


image = Image.open(requests.get(url, stream=True).raw)
# text = "How many cats are there?"
text = "What is the weather like?"

processor = ViltProcessor.from_pretrained("dandelin/vilt-b32-finetuned-vqa")
model = ViltForQuestionAnswering.from_pretrained("dandelin/vilt-b32-finetuned-vqa")

# prepare inputs
encoding = processor(image, text, return_tensors="pt")

# forward pass
outputs = model(**encoding)
logits = outputs.logits
idx = logits.argmax(-1).item()
print("Predicted answer:", model.config.id2label[idx])
