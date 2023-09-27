import os
from dotenv import load_dotenv
import googlemaps
from datetime import datetime, timedelta, timezone
import streamlit as st
from llm import extract_event_details

load_dotenv()
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

st.title('遅刻しなAI')

departure_point = st.text_input("出発地点:")
event_info = st.text_area("イベント情報:", height=200)

if st.button("計算"):
    
    place_response, times_response = extract_event_details(event_info)  # 関数を呼び出し
    arrival_point = place_response  # 到着地点にplace_responseを格納
    
    # times_responseをdatetimeオブジェクトに変換
    year, month, day, hour, minute, second = map(int, times_response.split(','))
    arrival_datetime = datetime(year, month, day, hour, minute, second) - timedelta(minutes=10)
    
    # UNIXタイムスタンプ計算
    jst_offset = timedelta(hours=9)  # JSTはUTC+9
    arrival_datetime = arrival_datetime.replace(tzinfo=timezone.utc)  # UTCにセット
    # arrival_datetime = arrival_datetime + jst_offset  # JSTに変換
    unix_timestamp = int(arrival_datetime.timestamp())
    
    # 座標を取得
    departure_location = gmaps.geocode(departure_point)
    arrival_location = gmaps.geocode(arrival_point)
    
    departure_lat_lng = f"{departure_location[0]['geometry']['location']['lat']},{departure_location[0]['geometry']['location']['lng']}"
    arrival_lat_lng = f"{arrival_location[0]['geometry']['location']['lat']},{arrival_location[0]['geometry']['location']['lng']}"
    
    # URL生成
    google_maps_url = f"https://www.google.com/maps/dir/{departure_lat_lng}/{arrival_lat_lng}/am=t/data=!4m9!4m8!1m1!4e1!1m0!2m3!6e1!7e2!8j{unix_timestamp}!3e3?entry=ttu"
    
    # st.write(f"出発地点座標: {departure_lat_lng}")
    # st.write(f"到着地点座標: {arrival_lat_lng}")
    # st.write(f"UNIXタイムスタンプ: {unix_timestamp}")
    st.write(f"Google Maps URL: {google_maps_url}")
    
