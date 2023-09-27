import os
from dotenv import load_dotenv
import openai
from datetime import datetime

# APIの初期設定
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def extract_event_details(input_event_data):

    current_year = datetime.now().year

    place_prompt = f'''
    Overview:
    Review the event details from the provided text and extract only the event location.

    Steps:

    Extract event details from the text.

    Retrieve location or meeting place details.
    Prioritize precise names of places or addresses for the location field to ensure compatibility with Google Maps.
    If precise location details aren't available, use descriptive location details from the text.

    Parameters:

    location: Precise name of the place or address, ensuring compatibility with Google Maps. Use descriptive details only if precise details aren't available.
    Output:
    Display the place of the extracted event.


    Input:
    {input_event_data}
    '''

    times_prompt = f'''
    Overview:
    Extract Google Calendar event details from the text provided and extract the event place.

    Steps:

    Extract event details from the text.


    Parameters:

    dates: Event start times. 
    If the year number cannot be confirmed, {current_year} should be used.

    Output:
    Output the extracted event start time in the format "YYYYY,MM,DD,HH,MM,SS".

    Example of output format:
    Output is for September 28, 2023 at 19:00
    2023, 9, 28, 19, 00, 00


    Input:
    {input_event_data}
    '''



    # モデルを呼び出し、レスポンスを取得
    place_response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=place_prompt,
        temperature=0,
        max_tokens=1000
    )

    # レスポンスからテキスト部分を取り出す
    place_response = place_response.choices[0].text.strip()

    if place_response.startswith("Output:\n\n"):
        place_response = place_response[len("Output:\n\n"):]
        

    # print(place_response)

    # モデルを呼び出し、レスポンスを取得
    times_response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=times_prompt,
        temperature=0,
        max_tokens=1000
    )

    # レスポンスからテキスト部分を取り出す
    times_response = times_response.choices[0].text.strip()

    if times_response.startswith("Output:\n\n"):
        times_response = times_response[len("Output:\n\n"):]

    if times_response.startswith("Output:\n"):
        times_response = times_response[len("Output:\n"):]


    # print(times_response)
    
    return place_response, times_response