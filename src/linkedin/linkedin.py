from langchain.chat_models import init_chat_model
import http.client
import os

conn = http.client.HTTPSConnection("linkedin-data-api.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "6d1442a489mshccb38dca71d2ca5p12253ajsndc8acfc924bb",
    'x-rapidapi-host': "linkedin-data-api.p.rapidapi.com"
}

openai_api_key = os.environ.get("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
os.environ["OPENAI_API_KEY"] = openai_api_key

gpt_4o = init_chat_model("gpt-4o", model_provider="openai", temperature=0)


def get_linkedin_profile_data(username: str):
    conn.request("GET", f"/?username={username}", headers=headers)
    res = conn.getresponse()
    data = res.read()

    #print(data.decode("utf-8"))
    
    respoonse = gpt_4o.invoke("Analyze the followling LinkedIn Data and summarize it. Make sure you include the email of the candidate in your response. " + data.decode("utf-8"))
    print(respoonse.content)
    return respoonse.content




    







