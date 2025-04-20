from langchain.chat_models import init_chat_model
import http.client
import os
import json
from fastapi import HTTPException
import os
import httpx

conn = http.client.HTTPSConnection("linkedin-data-api.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "bfbd3943cdmshfcd1edd8b659221p1d584fjsn7fea507d10aa",
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
    respoonse = gpt_4o.invoke("Analyze the followling LinkedIn Data and summarize it." + data.decode("utf-8"))
    print(respoonse.content)
    return respoonse.content

def get_profile_posts(username: str):
    conn.request("GET", f"/get-profile-posts?username={username}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    response = gpt_4o.invoke(
        "Analyze the following LinkedIn Posts and summarize them. "
        + data.decode("utf-8")
    )
    data_str = data.decode("utf-8")

    return response.content

def fetch_linkedin_profile_likes(username: str, start: int = 0) -> str:
    """
    Fetches LinkedIn profile likes for the given username, extracts the text
    from the latest 5 liked items, and saves it to likes.txt.

    :param username: LinkedIn username (e.g., "adamselipsky")
    :param start:    Offset for pagination (default: 0)
    :return:         A string containing the text of the latest 5 likes,
                     separated by newlines, or an error message.
    """
    conn = http.client.HTTPSConnection("linkedin-data-api.p.rapidapi.com")
    path = f"/get-profile-likes?username={username}&start={start}"
    combined_text_output = "Error: Could not fetch or process data." # Default error

    try:
        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        data_bytes = res.read()
        raw_json_string = data_bytes.decode("utf-8")

        # Parse the JSON response
        parsed_data = json.loads(raw_json_string)

        # Check if the response was successful and contains the expected data structure
        if parsed_data.get("success") and "data" in parsed_data and "items" in parsed_data["data"]:
            items = parsed_data["data"]["items"]

            # Get the latest 5 items (assuming the API returns them in chrono-descending order)
            latest_5_items = items[:5] # Slice the list to get the first 5

            # Extract the 'text' field from each of the latest 5 items
            # Use .get() to avoid errors if 'text' key is missing
            latest_5_texts = [item.get("text", "") for item in latest_5_items if item.get("text")]

            # Combine the texts into a single string, separated by a clear delimiter
            combined_text_output = "\n\n--- Post Separator ---\n\n".join(latest_5_texts)

        else:
            error_message = f"API Error or unexpected structure: {parsed_data.get('message', 'No message provided')}"
            print(error_message)
            combined_text_output = error_message
            # Save error message to file

    except json.JSONDecodeError:
        error_message = f"Error: Could not decode JSON response.\nRaw Response:\n{raw_json_string[:500]}..." # Show partial raw response for debugging
        print(error_message)
        combined_text_output = error_message
    except http.client.HTTPException as e:
        error_message = f"HTTP Error: {e}"
        print(error_message)
        combined_text_output = error_message
    except Exception as e:
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)
        combined_text_output = error_message
    finally:
        conn.close() # Ensure connection is cld

    return combined_text_output





