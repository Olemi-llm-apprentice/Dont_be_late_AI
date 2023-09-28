import os
from dotenv import load_dotenv
import openai
from datetime import datetime, timedelta
import re

# APIの初期設定
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def extract_event_details(input_event_data):

    
    current_datetime = datetime.now()

    # current_year = datetime.now().year
    #If the year number cannot be confirmed, {current_year} should be used.
    
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
    If the year, month, etc. cannot be confirmed, {current_datetime} is used as the current time for reference.

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

    # times_responseをdatetimeオブジェクトに変換
    year, month, day, hour, minute, second = map(int, times_response.split(','))
    times_response = datetime(year, month, day, hour, minute, second)

    # UTCに変換（日本時間はUTC+9）
    utc_start_time = times_response - timedelta(hours=9)
    utc_end_time = utc_start_time + timedelta(hours=2)

    # 新しい形式に変換
    jp_start_time_str = utc_start_time.strftime("%Y%m%dT%H%M%SZ")
    jp_end_time_str = utc_end_time.strftime("%Y%m%dT%H%M%SZ")
    Sample_Scheduled_time = jp_start_time_str + "/" + jp_end_time_str
    
    
    event_prompt = f'''
    Google Calendar URL Creation Template

    Overview:
    Guide to create a Google Calendar event URL from provided text. The aim is to extract and convert event details into a structured URL format, avoiding redundancy and ensuring clarity.

    Steps:

    Extract event details from the text.

    Retrieve location or meeting place details.
    Prioritize precise names of places or addresses for the location field to ensure compatibility with Google Maps.
    If precise location details aren't available, use descriptive location details from the text.

    Synthesize a title:

    Generate a comprehensive title based on the input content and extracted information. Avoid including the location in the title to prevent redundancy.

    Convert details to Google Calendar URL parameters:

    Default timezone is Asia/Tokyo unless specified.
    The start time of the event is determined by {times_response} and is expressed as {jp_start_time_str} considering the time zone.
    If the end time isn't provided, make an educated guess based on the event type (e.g., for lunch, it is 2 hours and is represented as {Sample_Scheduled_time}).
    
    Parameters:

    text: Generated event title that's comprehensive and non-redundant.
    dates: Event start and end times. Convert Asia/Tokyo time to UTC, considering a 9-hour difference unless otherwise mentioned.
    details: Event details link, which can be web page URLs or Zoom links. Reconstruct the details in a coherent manner, considering the intent and context of the provided information.
    location: Precise name of the place or address, ensuring compatibility with Google Maps. Use descriptive details only if precise details aren't available.
    trp: Set to false.
    Output:
    Google Calendar event URL matching the input text language.

    Input:
    {input_event_data}    '''
    
    
    
    # print(times_response)
    
        # モデルを呼び出し、レスポンスを取得
    event_response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=event_prompt,
        temperature=0,
        max_tokens=1500
    )
    
    event_response = event_response.choices[0].text.strip()
    
    if event_response.startswith("Output:\n\n"):
        event_response = event_response[len("Output:\n\n"):]

    if event_response.startswith("Output:\n"):
        event_response = event_response[len("Output:\n"):]

    if event_response.startswith("Output:"):
        event_response = event_response[len("Output:\n"):]
        
    if ' ' in event_response or '　' in event_response:
        event_response = re.sub(r'[ 　]', '', event_response)
    else:
        event_response = event_response
    
    return place_response, times_response, event_response

def calendar_registration(input_event_data):

    current_datetime = datetime.now()

    times_prompt = f'''
    Overview:
    Extract Google Calendar event details from the text provided and extract the event place.

    Steps:

    Extract event details from the text.


    Parameters:

    dates: Event start times. 
    If the year, month, etc. cannot be confirmed, {current_datetime} is used as the current time for reference.

    Output:
    Output the extracted event start time in the format "YYYYY,MM,DD,HH,MM,SS".

    Example of output format:
    Output is for September 28, 2023 at 19:00
    2023, 9, 28, 19, 00, 00


    Input:
    {input_event_data}
    '''

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

    # times_responseをdatetimeオブジェクトに変換
    year, month, day, hour, minute, second = map(int, times_response.split(','))
    times_response = datetime(year, month, day, hour, minute, second)

    # UTCに変換（日本時間はUTC+9）
    utc_start_time = times_response - timedelta(hours=9)
    utc_end_time = utc_start_time + timedelta(hours=2)

    # 新しい形式に変換
    jp_start_time_str = utc_start_time.strftime("%Y%m%dT%H%M%SZ")
    jp_end_time_str = utc_end_time.strftime("%Y%m%dT%H%M%SZ")
    Sample_Scheduled_time = jp_start_time_str + "/" + jp_end_time_str
    
    
    event_prompt = f'''
    Google Calendar URL Creation Template

    Overview:
    Guide to create a Google Calendar event URL from provided text. The aim is to extract and convert event details into a structured URL format, avoiding redundancy and ensuring clarity.

    Steps:

    Extract event details from the text.

    Retrieve location or meeting place details.
    Prioritize precise names of places or addresses for the location field to ensure compatibility with Google Maps.
    If precise location details aren't available, use descriptive location details from the text.

    Synthesize a title:

    Generate a comprehensive title based on the input content and extracted information. Avoid including the location in the title to prevent redundancy.

    Convert details to Google Calendar URL parameters:

    Default timezone is Asia/Tokyo unless specified.
    The start time of the event is determined by {times_response} and is expressed as {jp_start_time_str} considering the time zone.
    If the end time isn't provided, make an educated guess based on the event type (e.g., for lunch, it is 2 hours and is represented as {Sample_Scheduled_time}).
    
    Parameters:

    text: Generated event title that's comprehensive and non-redundant.
    dates: Event start and end times. Convert Asia/Tokyo time to UTC, considering a 9-hour difference unless otherwise mentioned.
    details: Event details link, which can be web page URLs or Zoom links. Reconstruct the details in a coherent manner, considering the intent and context of the provided information.
    location: Precise name of the place or address, ensuring compatibility with Google Maps. Use descriptive details only if precise details aren't available.
    trp: Set to false.
    Output:
    Google Calendar event URL matching the input text language.

    Input:
    {input_event_data}    '''
    
    
    
    # print(times_response)
    
        # モデルを呼び出し、レスポンスを取得
    event_response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=event_prompt,
        temperature=0,
        max_tokens=1500
    )
    
    event_response = event_response.choices[0].text.strip()
    
    if event_response.startswith("Output:\n\n"):
        event_response = event_response[len("Output:\n\n"):]

    if event_response.startswith("Output:\n"):
        event_response = event_response[len("Output:\n"):]

    if event_response.startswith("Output:"):
        event_response = event_response[len("Output:\n"):]
        
    if ' ' in event_response or '　' in event_response:
        event_response = re.sub(r'[ 　]', '', event_response)
    else:
        event_response = event_response
    
    return event_response
