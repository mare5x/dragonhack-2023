# dragonhack-2023

DragonHack 2023 submission by Team LeMoNS (Leon, Marko, Nace, Sara).

## About

> Our chatbot helps users pick the best spot for a trip based on real-time webcam data. It provides weather forecasts, webcam images and answers using Visual-Question Answering. It can provide data for a specific location (_How many boats are in Koper Marina?_) or make recommendations fitting user requirements (_Where is there snow?_).

### Technical details

#### Backend
- The backend is written in Python using **Flask**.
- For parsing user input we use OpenAI's **ChatGPT API**, which transforms unstructured data into JSON objects.
- **Live webcam feeds** are fetched from ARSO and [hribi.net](https://www.hribi.net/).
- A local **visual question answering model from HuggingFace** (_dandelin/vilt-b32-finetuned-vqa_) is used for answering queries about webcams.
- Additional weather forecast data is provided by a public **weather API**.

#### Frontend
- HTML + JS + CSS. That's it.


## Setup

### Backend

1. Install the required packages:
```
python -m venv .env
source ./.env/bin/activate  # linux
./.env/Scripts/activate  # windows

pip install -r requirements.txt
```

2. Run the server:
```
flask run
```

### Frontend

1. `npm install` (first time only)
2. `npm start`
3. [http://localhost:8080/](http://localhost:8080/)
