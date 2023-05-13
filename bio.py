import requests


prompt = "Write a haiku about DragonHack."
model = "gpt-3.5-turbo"
#token = "rehvDn6zukf53UQG9W0xZ4WRTsmDV4"
token = "VJ7c9CyPPsSgcJpbgWVfpUkG1s4jHN"

response = requests.post(
   "https://openai-api.meetings.bio/api/openai/chat/completions",
   headers={"Authorization": f"Bearer {token}"},
   json={
       # specification of all options: https://platform.openai.com/docs/api-reference/chat/create
       "model": model,
       "messages": [{"role": "user", "content": prompt}],
   },
)


if response.ok:
   print(response.json()["choices"][0]["message"]["content"])

