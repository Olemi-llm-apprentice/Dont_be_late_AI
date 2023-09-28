import os
from dotenv import load_dotenv
import googlemaps
from datetime import datetime, timedelta, timezone
import streamlit as st
from llm import extract_event_details
# import pandas as pd


load_dotenv()
gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))

st.set_page_config(
    page_title="遅刻しなAI",  # Set the browser tab title to "My App"
)

st.title('遅刻しなAI')
st.write("このアプリは予定通知メールなどの本文からコピペでカレンダー登録と予定地までの電車経路のURLを生成するアプリです。")
st.markdown("**スマホの場合Chromeブラウザで開くとアプリ遷移がスムーズになるかもしれません**")

departure_point = st.text_input("出発地点:", placeholder="住所または新宿駅など駅名を入力")
# st.caption("住所や新宿駅など駅名を入力")
event_info = st.text_area("予定情報:", placeholder="スケジュール内容をコピペ\n予定名：全日本模型ホビーショー\n場所：東京ビッグサイト 南1・2ホール\n日時：2023年9月30日 14:00\n\nまたは日付けと目的地が入った文章を入力\n10/15 18時から渋谷集合で", height=250)
# st.caption("スケジュール内容をコピペ → 予定名：全日本模型ホビーショー\n場所：東京ビッグサイト 南1・2ホール\n日時：2023年9月30日 14:00")
# st.caption("または日付けと目的地が入った文章を入力 → 10/15 18時から渋谷集合で")

if st.button("URL生成"):
    with st.spinner('生成処理中...'):
        place_response, times_response, event_response = extract_event_details(event_info)  # 関数を呼び出し
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
    st.write(f"Google Maps 乗換経路 URL: {google_maps_url}")
    st.write(f"Google Calendar 登録 URL:\n {event_response}")
    
    # departure_lat = departure_location[0]['geometry']['location']['lat']
    # departure_lon = departure_location[0]['geometry']['location']['lng']
    # arrival_lat = arrival_location[0]['geometry']['location']['lat']
    # arrival_lon = arrival_location[0]['geometry']['location']['lng']
    
    # map_data = pd.DataFrame({
    # 'lat': [departure_lat, arrival_lat],
    # 'lon': [departure_lon, arrival_lon]
    # })
    # st.map(map_data)
    
st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f1f1f1;
            text-align: center;
            padding: 10px;
        }
    </style>
    <div class="footer">
        <p>問い合わせはこちらまで: <a href="https://twitter.com/lemilemilemio" target="_blank">https://twitter.com/lemilemilemio</a></p>
    </div>
    """, unsafe_allow_html=True)
    
