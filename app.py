import re
from flask import Flask, request, jsonify
import requests
import time
from datetime import datetime, timedelta
import sqlite3
from requests.exceptions import Timeout
import logging

app = Flask(__name__)

# Configure the logger
logging.basicConfig(filename='myapp.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to fetch data from SQLite
def fetch_data_from_database():
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    cursor.execute('select GR_TOKEN from Account where username = "vngetlink1"')
    data = cursor.fetchall()
    conn.close()
    return data


# [hienhd]
# Show all data from table

# Function to fetch data from SQLite
def show_all_data_from_database():
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    cursor.execute('select * from Account')
    data = cursor.fetchall()
    conn.close()
    return data

@app.route('/showalldata', methods=['GET'])
def show_all_data():
    rsData = show_all_data_from_database()
    return jsonify({"data": rsData}), 200

# [hienhd]
# Get webtoken from 1 account

# Function to fetch data from SQLite
def fetch_webtoken_from_database(site, typelink):
    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    query = 'select webtoken from Account where site = "' + site + '" and type = "' + typelink + '"' 
    cursor.execute(query)
    data = cursor.fetchone()
    conn.close()
    return data[0]

@app.route('/getwebtoken', methods=['POST'])
def get_webtoken_data():
    data = request.get_json()
    site = data['site']
    typelink = data['typelink']

    rsData = fetch_webtoken_from_database(site, typelink)
    return jsonify({"data": rsData}), 200

# [hienhd]
# Update webtoken with 1 account

# Function to fetch data from SQLite
def update_webtoken_to_database(webtoken, username, site, typelink):

    create_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    conn = sqlite3.connect('account.db')
    cursor = conn.cursor()
    query = 'UPDATE Account SET webtoken = "' + webtoken + '", create_time = "' + create_time + '" where username = "' + username + '" and site = "' + site + '" and type = "' + typelink + '"'
    try:
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(e)
        conn.close()
        return False
    
@app.route('/updateWebToken', methods=['PUT'])
def update_web_token():
    data = request.get_json()
    webtoken = data['webtoken'] 
    username = data['username']
    site = data['site']
    typelink = data['typelink']

    rsData = update_webtoken_to_database(webtoken, username, site, typelink)
    return jsonify({"success": rsData}), 200


# [hienhd]
# Get link photo freebik with 1 account

csrf_token = "220bc3ec7838404a4d1eba129951a33c"

def getIdentityAPI(csrf_freepik, link, cookie_request):
    
    data = {}
    headers = {
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "Cookie": cookie_request,
                    "Referer": link,
                    "X-Csrf-Token": csrf_freepik,
                    "X-Requested-With": "XMLHttpRequest"
                }    
    
    url = "https://www.freepik.com/user/device-manager/identify"

    try:
        response = requests.post(url, json=data, headers=headers, timeout=5)
        if response.status_code == 200:
            rs = response.json()
            print(rs)
            if rs['success'] == True:
                csrf_token = rs['csrfToken']
                return csrf_token
            else:
                return csrf_freepik

        else:
            print("Error get new_csrf_token: ", response.status_code)
            return csrf_freepik
        
    except Timeout:
        # Handle the timeout exception here
        return csrf_freepik

def getFreebikPhotoAPI(link, id, csrf_freepik):

    global csrf_token

    # Get cookie from many Account
    #cookie_request = "_tt_enable_cookie=1; _pin_unauth=dWlkPU1tTXpNREV3WkdZdE5HRTFaQzAwTUdGakxXSmxZemt0TUROalpURTVOamsyT1RKbA; OptanonAlertBoxClosed=2023-09-05T12:40:31.980Z; CONTRIBUTOR_FR_REFRESH=AMf-vBwv36u7ectvZKBFnZN0yAh_2dDI3A_4QAaN9X9-A8IG10sImeK2nqHxaonjHuSw_cWWSE0w5ENHvOaWdyy1wW_1wzPfnsMPv000s11vTC8kx8KAzF5IAq-r0qI_iIaMG3sXkUGMooMz7XYccVO8oiB7N0eg8w5o4s5we6FOBW2EbQVupc6Wl1viFMaTo6UpLJM556W4; ads-tag=b; _lr_geo_location_state=HN; _lr_geo_location=VN; g_state={'i_l':1,'i_p':1694096145670}; GR_REFRESH=AMf-vBy3TC0-E4Mcqn9pEhug14AhRTM-hH-ZhELeKj31zsm49Xj9AI1QPVZOfIFjpBR6goNuh3cdDZ0UHiPN_c0KTRtZEv4pQFsHkXqKwm4YYZlGcbIzE-OK0hS9-klOKu9CcVo2vxF52ft7ssxFc3K5-RTNT8lPWidlgQOYQ4eqdm6qDKsztCKVn8IbEUzuFW2MiqxvXBfh; GRID=99979591; ol-OL_Tracking_ID=99979591; G_ENABLED_IDPS=google; notify--autopromo-coupon=1; GR_TOKEN=eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5MGFkMTE4YTk0MGFkYzlmMmY1Mzc2YjM1MjkyZmVkZThjMmQwZWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTElOSyBHRVQiLCJwaWN0dXJlIjoiaHR0cHM6Ly9hdmF0YXIuY2RucGsubmV0L2RlZmF1bHRfMDgucG5nIiwiYWNjb3VudHNfdXNlcl9pZCI6OTk5Nzk1OTEsInNjb3BlcyI6ImZyZWVwaWsvaW1hZ2VzIGZyZWVwaWsvdmlkZW9zIGZsYXRpY29uL3BuZyBmcmVlcGlrL2ltYWdlcy9wcmVtaXVtIGZyZWVwaWsvdmlkZW9zL3ByZW1pdW0gZmxhdGljb24vc3ZnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2ZjLXByb2ZpbGUtcHJvLXJldjEiLCJhdWQiOiJmYy1wcm9maWxlLXByby1yZXYxIiwiYXV0aF90aW1lIjoxNjk0MDg5MDE5LCJ1c2VyX2lkIjoiM1k2SEJyWGlxRmRjcHZzMExYQmd5UkVWNjJoMiIsInN1YiI6IjNZNkhCclhpcUZkY3B2czBMWEJneVJFVjYyaDIiLCJpYXQiOjE2OTQxMzk5MTUsImV4cCI6MTY5NDE0MzUxNSwiZW1haWwiOiJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMDQ4NDQ4ODg2MzEwNjUzNDM2NCJdLCJlbWFpbCI6WyJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.HWhOgBBbPCGh0ZGP_34T_XpSSj1S3HrI6d15uJWQ7yc6CbEf_w7Jy6o1bdxtv6VcSokSO1htdwAVKWaIP8qsfeduT87LFvZm3pJoqJ-RF5wgV8_iiQWR-OYMtCzhn5WHUv-NcZaNNdRiKu5xR_X5VGHpcdcxwwt36QPdTWMThPLWUG8srDqWQNIBCGQe8Df9izUv8jBUNj-qBXta0cnTDtRr6qBMrcuDpDDN5TuzHMNxsqYDBw-2h2f5IVoJfyhnZRUrcW1v6ygn_TwDXs8Sc39aKX4iTg2zG1-oBnxKI40rfjkuHooYLPHlX4DfnKqegsEQoTBi5M0cSCl3WzUY1w; csrf_freepik=" + csrf_freepik + "; autopromo-visit={'p_ud':1694106180154,'p_vt':16}; ol-OL_LIB_INSTALL_TIME=1694112912683; refmodal=" + link + "#from_view=detail_author;"
    cookie_request = "_tt_enable_cookie=1; OptanonAlertBoxClosed=2023-09-05T12:40:31.980Z; ads-tag=b; _lr_geo_location_state=HN; _lr_geo_location=VN; g_state={'i_l':1,'i_p':1694096145670}; GR_REFRESH=AMf-vBy3TC0-E4Mcqn9pEhug14AhRTM-hH-ZhELeKj31zsm49Xj9AI1QPVZOfIFjpBR6goNuh3cdDZ0UHiPN_c0KTRtZEv4pQFsHkXqKwm4YYZlGcbIzE-OK0hS9-klOKu9CcVo2vxF52ft7ssxFc3K5-RTNT8lPWidlgQOYQ4eqdm6qDKsztCKVn8IbEUzuFW2MiqxvXBfh; GRID=99979591; ol-OL_Tracking_ID=99979591; G_ENABLED_IDPS=google; notify--autopromo-coupon=1; GR_TOKEN=eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5MGFkMTE4YTk0MGFkYzlmMmY1Mzc2YjM1MjkyZmVkZThjMmQwZWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTElOSyBHRVQiLCJwaWN0dXJlIjoiaHR0cHM6Ly9hdmF0YXIuY2RucGsubmV0L2RlZmF1bHRfMDgucG5nIiwiYWNjb3VudHNfdXNlcl9pZCI6OTk5Nzk1OTEsInNjb3BlcyI6ImZyZWVwaWsvaW1hZ2VzIGZyZWVwaWsvdmlkZW9zIGZsYXRpY29uL3BuZyBmcmVlcGlrL2ltYWdlcy9wcmVtaXVtIGZyZWVwaWsvdmlkZW9zL3ByZW1pdW0gZmxhdGljb24vc3ZnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2ZjLXByb2ZpbGUtcHJvLXJldjEiLCJhdWQiOiJmYy1wcm9maWxlLXByby1yZXYxIiwiYXV0aF90aW1lIjoxNjk0MDg5MDE5LCJ1c2VyX2lkIjoiM1k2SEJyWGlxRmRjcHZzMExYQmd5UkVWNjJoMiIsInN1YiI6IjNZNkhCclhpcUZkY3B2czBMWEJneVJFVjYyaDIiLCJpYXQiOjE2OTQxMzk5MTUsImV4cCI6MTY5NDE0MzUxNSwiZW1haWwiOiJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMDQ4NDQ4ODg2MzEwNjUzNDM2NCJdLCJlbWFpbCI6WyJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.HWhOgBBbPCGh0ZGP_34T_XpSSj1S3HrI6d15uJWQ7yc6CbEf_w7Jy6o1bdxtv6VcSokSO1htdwAVKWaIP8qsfeduT87LFvZm3pJoqJ-RF5wgV8_iiQWR-OYMtCzhn5WHUv-NcZaNNdRiKu5xR_X5VGHpcdcxwwt36QPdTWMThPLWUG8srDqWQNIBCGQe8Df9izUv8jBUNj-qBXta0cnTDtRr6qBMrcuDpDDN5TuzHMNxsqYDBw-2h2f5IVoJfyhnZRUrcW1v6ygn_TwDXs8Sc39aKX4iTg2zG1-oBnxKI40rfjkuHooYLPHlX4DfnKqegsEQoTBi5M0cSCl3WzUY1w; csrf_freepik=" + csrf_freepik + "; autopromo-visit={'p_ud':1694106180154,'p_vt':16}; ol-OL_LIB_INSTALL_TIME=1694112912683; refmodal=" + link + "#from_view=detail_author;"

    headers = {
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "Cookie": cookie_request,
                    "Referer": link,
                    "X-Csrf-Token": csrf_freepik,
                    "X-Requested-With": "XMLHttpRequest"
                }

    url = "https://www.freepik.com/xhr/download-url/" + id + "?token=03ADUV_6d_BNvTbB4JUdAcL1H-P2fwuqBmUNn5JW_CRI3a3eOUX2qRr0yPOYqbtKxGUT2OdbKNirumF-9D_Mc7uW6LZ1mMZn6S_AqRp8TeFXV_ZNPh79NBOsCXG5lWwbNmRnVs-foo_854_NV6zZM8KfwGy93Cpk9c97_duoOnPSe0pvypSQ99BwZN9jtNvqXeARv8STWj-vAiYjTxS0_eAjCzKd1CH_7gvO0DZWkGeVgCDAfrp9vmFOEqwQk7iytva13O1-K55tzLxcan6pXY8OMsxPsb81v_zaV5ZVrLgFjX0fpL21Dz8lMSxp2zVpATdq0U3iU3u_ViouQxdid7iNFFjFpOAKpHUzlAUt3uJ0dz_jDn_ec208ADyF5xlcPRcZYWeTtOyieEOMxveILiOovVpBAGJ3EeflihdZ1lehyT9bp_9RuGw3FzYvmjK-qFSH8Eso0C6mT1USi-wexf5DxhiXU89WH4btL0bEIjIekW4uVFLl46x4JPQLtL4zHhoHqCjZUDC2jShOcCQABCuktPQkqAZ6Bets2_0s375ca57sInLU4Buvi5iWLsD9L7--kufD01y30j1MY8qEu6V1zmc4vaDtsZjH6LJLiAUjej62hT1Y1vGHO3yAq7BzsHX8w2eTr1RQWjPrdz9bcekqmqnuWal1cCCKZ2ysa5-jEbnFtSFr7tBUqrmdJmVEQf594XGB7TCd1rEX6GHNX5jFAJk0Q7NhzZRSm4iAgBQh0wI6tO5Jf2maVSof9glAKZBFUDDSYlLj-du_hY2J90TgcoaHgIa0dBedH8cBX_FTLhMTCSGiSEHlwE5h3QJotodQtQbvevitq0qlqeU5gibmHIn-AYhUvFUOsyExmFngJUwl_v4c2ik7PZZ-SJGcHrtS4mukd4K33L_jT9JVtoRrMNjzS47dNNUCPzqX8Qx_dq3Banjul8srrlwrl34MGjnp3qrAdAp9-dwCN_sBip7dZbJ1uGIkpk8LWqTfEuVNuQQD8-Ox6X7aQbyXKBUCVuoBRmfpZUmveXKsODYHnPHb_FqapZrASA2JDyxIwI3zGxMHBY0nymjmL2xah-lTku6lxAA_DfjU3PwSrkywHeY74iNidKrhdS4ihNYXuPB8PQfRbvYfWPFjuizL7Ud62JYB3H8HWQtFChjd0ef3KmPKlUAQyOrtHr2MD2Bd7QxC0a05lQJLLk_iSDVorRPc0TM-6QmBr3giQtIHWUBlOkppQskCXENY_ntsZRGJ-YEK7KcqUrpaIr3xiJaZC92aPrN9_stb3JCHpR-NthAGvc3ckq44Zp0Ru9yykoDy2TKJZtqxxnp6Fa4IBop2Ak_QBr7_oWIRiNn6wZ6sCwg47C0xxzhtAkPJI5dszSC47hA2WqhaW8PLQTfK6yrNt8Et7mKj36i3S4UUloOXJvFj_3n3E-SQ4GGebQI8WWXOW6upagnuHbv0f1MsDXjSjU3WUrKXXlq_8QDbIEhXpr54tBRiMqat8YUlt0gA1TSJwOaLnEfVLGHX_NcJUwXlJrDWp8idZH171BjV2rcSE31TrmOe9WzQqWxTEq4hwSLXvoZymmqqmzHfNR_Qk"

    countRetry = 1
    while countRetry <= 5:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                rs = response.json()
                
                if rs['success'] == True:
                    # Get identity and revc() csrf_token
                    csrf_token = getIdentityAPI(csrf_freepik, link, cookie_request)
                    return {'result': 'success', 'message': rs}
                else:
                    time.sleep(0.5)
                    countRetry = countRetry + 1

            else:
                print("Error: ", response.status_code)
                logging.error(f"Freebik photo error occurred - Status Code: {response.status_code}")
                time.sleep(0.5)
                countRetry = countRetry + 1
        
        except Timeout:
            # Handle the timeout exception here
            return {'result': 'error', 'message': 'Request timed out'}

    return {'result': 'error', 'message': 'Get link fail'}

@app.route('/getFreebikPhoto', methods=['POST'])
def get_freebik_photo():
    
    data = request.get_json()
    link = data['link'] 
    id = data['id']

    if 'x-csrf-token' not in data and data['x-csrf-token'] == 'vngetlink2023' and (link == '' or id == ''):
        return jsonify({'result': 'error', 'message': 'Authentication is required'}), 200
    
    rsData = getFreebikPhotoAPI(link, id, csrf_token)
    
    return jsonify(rsData), 200


# [hienhd]
# Get link video freebik with 1 account

def refreshGRToken(link):

    url = 'https://www.freepik.com/xhr/user/last-failed-payment'

    if link == "":
        link = "https://www.freepik.com/premium-video/focused-person-works-studies-laptop-computer-balcony-city_387505"

    grtoken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5MGFkMTE4YTk0MGFkYzlmMmY1Mzc2YjM1MjkyZmVkZThjMmQwZWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTElOSyBHRVQiLCJwaWN0dXJlIjoiaHR0cHM6Ly9hdmF0YXIuY2RucGsubmV0L2RlZmF1bHRfMDgucG5nIiwiYWNjb3VudHNfdXNlcl9pZCI6OTk5Nzk1OTEsInNjb3BlcyI6ImZyZWVwaWsvaW1hZ2VzIGZyZWVwaWsvdmlkZW9zIGZsYXRpY29uL3BuZyBmcmVlcGlrL2ltYWdlcy9wcmVtaXVtIGZyZWVwaWsvdmlkZW9zL3ByZW1pdW0gZmxhdGljb24vc3ZnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2ZjLXByb2ZpbGUtcHJvLXJldjEiLCJhdWQiOiJmYy1wcm9maWxlLXByby1yZXYxIiwiYXV0aF90aW1lIjoxNjk0MDg5MDE5LCJ1c2VyX2lkIjoiM1k2SEJyWGlxRmRjcHZzMExYQmd5UkVWNjJoMiIsInN1YiI6IjNZNkhCclhpcUZkY3B2czBMWEJneVJFVjYyaDIiLCJpYXQiOjE2OTQ1NzY1ODQsImV4cCI6MTY5NDU4MDE4NCwiZW1haWwiOiJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMDQ4NDQ4ODg2MzEwNjUzNDM2NCJdLCJlbWFpbCI6WyJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.h-ek6X7ZrDhN1IjSrPF0z_iuhoAxWFNiAM0pb3D0tiotqhNnfMQX7zJKS8tHrcC8JyzbGh4cDshLYXDGUOUg3Cclcf5vrwCQxBgXcPLo8IFtObOTblDPGOeCp27a1h0xXDjTYbKXp8qIS-sWJ96O9Q7V6g0H30J-JQrstd3MAFh-WZjMsBfEec5G0LDfvHDl3PXrOB_5PTlnOwtYun_4E12HoXiAWaHjeAvkOVftdeE1U4ei8hSZlOtoVJGUxgp5xClQrbIS4k2HEq2hDPoOQP5mNm4dP6SeGfA328V-w84XqaH2BfJ29SeY6swwSfrTveNpvVq9CvtkU7H4adnD2A"
    
    cookie_request = "_fcid=FC.d616a023-cdd0-7789-2741-bf433ed66354; _tt_enable_cookie=1; _pin_unauth=dWlkPU1tTXpNREV3WkdZdE5HRTFaQzAwTUdGakxXSmxZemt0TUROalpURTVOamsyT1RKbA; OptanonAlertBoxClosed=2023-09-05T12:40:31.980Z; CONTRIBUTOR_FR_REFRESH=AMf-vBwv36u7ectvZKBFnZN0yAh_2dDI3A_4QAaN9X9-A8IG10sImeK2nqHxaonjHuSw_cWWSE0w5ENHvOaWdyy1wW_1wzPfnsMPv000s11vTC8kx8KAzF5IAq-r0qI_iIaMG3sXkUGMooMz7XYccVO8oiB7N0eg8w5o4s5we6FOBW2EbQVupc6Wl1viFMaTo6UpLJM556W4; ads-tag=b; _lr_geo_location_state=HN; _lr_geo_location=VN; g_state={'i_l':1,'i_p':1694096145670}; GR_REFRESH=AMf-vBy3TC0-E4Mcqn9pEhug14AhRTM-hH-ZhELeKj31zsm49Xj9AI1QPVZOfIFjpBR6goNuh3cdDZ0UHiPN_c0KTRtZEv4pQFsHkXqKwm4YYZlGcbIzE-OK0hS9-klOKu9CcVo2vxF52ft7ssxFc3K5-RTNT8lPWidlgQOYQ4eqdm6qDKsztCKVn8IbEUzuFW2MiqxvXBfh; GRID=99979591; ol-OL_Tracking_ID=99979591; G_ENABLED_IDPS=google; notify--autopromo-coupon=1; GR_TOKEN=" + str(grtoken) + "; csrf_freepik=" + "36eb10131ef669b4c19f06d71ee7e5d4" + "; autopromo-visit={'p_ud':1694106180154,'p_vt':16}; ol-OL_LIB_INSTALL_TIME=1694112912683; refmodal=" + str(link)

    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5',
        'Accepts': 'application/json',
        'Content-Type': 'application/json',
        'Cookie': cookie_request,
        'Referer': link,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
        'X-Requested-With': 'xmlhttprequest'
    }

    countRetry = 1
    while countRetry <= 3:

        response = requests.get(url, headers=headers, timeout=5)
        # Get the "Set-Cookie" header value
        set_cookie_header = response.headers.get('Set-Cookie', '')
        # Use regular expressions to extract the value of the GR_TOKEN cookie
        match = re.search(r'GR_TOKEN=([^;]+)', set_cookie_header)

        if match:
            gr_token = match.group(1)
            print(f'GR_TOKEN: {gr_token}')
            return gr_token
        else:
            print('GR_TOKEN not found in the Set-Cookie header')
            countRetry = countRetry + 1
            time.sleep(0.5)

def getFreebikVideoAPI(link, id, GR_TOKEN):

    # Get cookie from many Account
    #GR_TOKEN = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5MGFkMTE4YTk0MGFkYzlmMmY1Mzc2YjM1MjkyZmVkZThjMmQwZWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTElOSyBHRVQiLCJwaWN0dXJlIjoiaHR0cHM6Ly9hdmF0YXIuY2RucGsubmV0L2RlZmF1bHRfMDgucG5nIiwiYWNjb3VudHNfdXNlcl9pZCI6OTk5Nzk1OTEsInNjb3BlcyI6ImZyZWVwaWsvaW1hZ2VzIGZyZWVwaWsvdmlkZW9zIGZsYXRpY29uL3BuZyBmcmVlcGlrL2ltYWdlcy9wcmVtaXVtIGZyZWVwaWsvdmlkZW9zL3ByZW1pdW0gZmxhdGljb24vc3ZnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2ZjLXByb2ZpbGUtcHJvLXJldjEiLCJhdWQiOiJmYy1wcm9maWxlLXByby1yZXYxIiwiYXV0aF90aW1lIjoxNjk0NTI1NTQyLCJ1c2VyX2lkIjoiM1k2SEJyWGlxRmRjcHZzMExYQmd5UkVWNjJoMiIsInN1YiI6IjNZNkhCclhpcUZkY3B2czBMWEJneVJFVjYyaDIiLCJpYXQiOjE2OTQ1MzA3MjIsImV4cCI6MTY5NDUzNDMyMiwiZW1haWwiOiJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMDQ4NDQ4ODg2MzEwNjUzNDM2NCJdLCJlbWFpbCI6WyJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.Hd426kFF7MYp2VsN1uUHnJK-wU16Xd0gw9yHIEp-DXBsAZjceNKfN9AeQW3BBpfKFNHjx-qARYib_JsojXMnwB785-J1omyuHNc5ikT4e_Yw5qmNouOLrRvMAhLE0CVhI6qq9g1vt-nzC4-zDE0JvSetkq7uhJriv3V7rEqHnKbbH-_kz88j6dJVqXVL67-jXnAtbIFahAqciLU34Fk-QbDzbuJp4hSlSod07nY_REGHiDE1qYQ-YUxSrzqjXsfAstXb603bFny-jT1Al834VjKQHVBnJLEXE37Xyn6OTLT7UGYhOGlSI9ZuEusdiFQEfmEV_c26UCSXoUygS_JrtA"    
    cookie_request = "_fcid=FC.d616a023-cdd0-7789-2741-bf433ed66354; _tt_enable_cookie=1; _pin_unauth=dWlkPU1tTXpNREV3WkdZdE5HRTFaQzAwTUdGakxXSmxZemt0TUROalpURTVOamsyT1RKbA; OptanonAlertBoxClosed=2023-09-05T12:40:31.980Z; CONTRIBUTOR_FR_REFRESH=AMf-vBwv36u7ectvZKBFnZN0yAh_2dDI3A_4QAaN9X9-A8IG10sImeK2nqHxaonjHuSw_cWWSE0w5ENHvOaWdyy1wW_1wzPfnsMPv000s11vTC8kx8KAzF5IAq-r0qI_iIaMG3sXkUGMooMz7XYccVO8oiB7N0eg8w5o4s5we6FOBW2EbQVupc6Wl1viFMaTo6UpLJM556W4; ads-tag=b; _lr_geo_location_state=HN; _lr_geo_location=VN; g_state={'i_l':1,'i_p':1694096145670}; GR_REFRESH=AMf-vBy3TC0-E4Mcqn9pEhug14AhRTM-hH-ZhELeKj31zsm49Xj9AI1QPVZOfIFjpBR6goNuh3cdDZ0UHiPN_c0KTRtZEv4pQFsHkXqKwm4YYZlGcbIzE-OK0hS9-klOKu9CcVo2vxF52ft7ssxFc3K5-RTNT8lPWidlgQOYQ4eqdm6qDKsztCKVn8IbEUzuFW2MiqxvXBfh; GRID=99979591; ol-OL_Tracking_ID=99979591; G_ENABLED_IDPS=google; notify--autopromo-coupon=1; GR_TOKEN=" + str(GR_TOKEN) + "; csrf_freepik=" + "36eb10131ef669b4c19f06d71ee7e5d4" + "; autopromo-visit={'p_ud':1694106180154,'p_vt':16}; ol-OL_LIB_INSTALL_TIME=1694112912683; refmodal=" + str(link)

    headers = {
                    "Accept": "application/json, text/plain, */*",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Content-Type": "application/json",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                    "Cookie": cookie_request,
                    "Referer": link
                }

    url = "https://www.freepik.com/api/video/download?optionId=" + id
    print(url)
    countRetry = 1
    while countRetry <= 1:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:
                rs = response.json()
                
                # Get identity and revc() csrf_token
                return {'result': 'success', 'message': rs}
                
            else:
                print("Error: ", response.status_code)
                logging.error(f"Freebik video error occurred - Status Code: {response.status_code}")
                if response.status_code == 401:
                    return {'result': 'error', 'message': '401'}

                time.sleep(0.5)
                countRetry = countRetry + 1

        except Timeout:
            logging.error("Request timed out")
            # Handle the timeout exception here
            return {'result': 'error', 'message': 'Request timed out'}
        
    return {'result': 'error', 'message': 'Get link fail'}

@app.route('/getFreebikVideo', methods=['POST'])
def get_freebik_video():

    data = request.get_json()
    link = data['link'] 
    id = data['id']

    if 'x-csrf-token' not in data and data['x-csrf-token'] == 'vngetlink2023' and (link == '' or id == ''):
        return jsonify({'result': 'error', 'message': 'Authentication is required'}), 200
    
    GR_TOKEN = fetch_webtoken_from_database("freebik", "video")
    #print(GR_TOKEN)
    rsData = getFreebikVideoAPI(link, id, GR_TOKEN)

    if rsData['result'] == 'error' and rsData['message'] == '401':
        GR_TOKEN = refreshGRToken(link)
        update_webtoken_to_database(GR_TOKEN, "vngetlink1", "freebik", "video")
        rsData = getFreebikVideoAPI(link, id, GR_TOKEN)
    
    return jsonify(rsData), 200



# [hienhd]
# Get link psd huaban with 1 account
def getMaterialsInfo(link, pinid, cookie_request):
    headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Cookie": cookie_request,
                "Referer": link,
            }

    url = "https://api.huaban.com/pins/" + str(pinid) + "?fields=pin:PIN_DETAIL&pins=20"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            rs = response.json()
            if 'material_info' in rs['pin']:
                print("material_id: ", rs['pin']['material_info']['id'])
                print("material_title: ", rs['pin']['material_info']['title'])
                print("material_format: ", rs['pin']['material_info']['origin_file_format'])
                return rs['pin']['file_material']['material_id'], rs['pin']['material_info']['title'], rs['pin']['material_info']['origin_file_format']
            else:
                print("Get material_info Error: Link is not contain Material")
                return "", "", ""

        else:
            print("Get material_info Error: ", response.status_code)
            return "", "", ""
        
    except Timeout:
        print("Get material_info Timeout...")
        return "", "", ""

def getHuabanPreDownload(link, materialsId, cookie_request):
    headers = {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Cookie": cookie_request,
                "Referer": link,
            }

    data = {
        'download_type': 1,
        'type': 4
    }

    url = "https://api.huaban.com/biz/materials/" + str(materialsId) + "/pre-download"
    print("Link Predownload: ", url)
    response = requests.post(url, json=data, headers=headers, timeout=5)
    if response.status_code == 200:
        rs = response.json()
        return rs
    else:
        print("Error: " + response.status_code)
        return {"vips": []}

def getHuabanDownload(link, pinid, materialsId, materialsTitle, materialsFormat, preDownload, cookie_request):
    print("Downloading VIP...")
    logging.info(f"Process: Downloading...")
    headers = {
                "Accept-Encoding": "gzip, deflate, br",
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
                "Cookie": cookie_request,
                "Referer": link,
            }

    payload = {
        "type": 4,
        "download_type": 1,
        "material_title": materialsTitle,
        "right_code": preDownload['rights'][0]['inspect']['right_code'],
        "system_code": preDownload['vips'][0]['system_code'],
        "vip_cert_subject_id": preDownload['rights'][0]['subject_info']['id'],
        "vip_name": preDownload['vips'][0]['vip']['title'],
        "order_no": preDownload['vips'][0]['card_no'],
        "vip_id": preDownload['vips'][0]['vip_id'],
        "pin_id": pinid,
        "filename": str(materialsTitle) + "_" + str(materialsId) + "." + str(materialsFormat),
        "material_type": materialsFormat,
        "fake_download": False
    }

    url = "https://api.huaban.com/biz/materials/" + str(materialsId) + "/download"

    response = requests.post(url, json=payload, headers=headers, timeout=5)
    if response.status_code == 200:
        rs = response.json()
        logging.info(f"Process: Downloading {link} success")
        return {'result': 'success', 'leftDownload': preDownload['rights'][0]['inspect']['left'], 'message': rs }
    else:
        print("Error")
        print(response.status_code)
        logging.error(f"Process: Downloading error {response.status_code}")
        return {'result': 'error', 'leftDownload': preDownload['rights'][0]['inspect']['left'], 'message': 'getHuabanDownload error...' + response.status_code}

def getHuabanPSDAPI(link, pinid):

    logging.info(f"Process getHuabanPSD: {link}")
    sid = "s%3AxGixdtv1wZ19XgGUxcofwtuWh-KP9fA-.mVugLje%2FXZsvMRqBst%2FAQcnZrTnVK%2F%2FKTb0aboBtPsQ"
    #sid = "s%3AuXKOGgmZho8wdQa6dgOCrzpu8N3134Nq.HadZaQzp0swR8F40N07w3r4WNVuj34bHnTLxXJmSRjY"
    cookie_request = "user_device_id=fe32db8dd4c24808bf93457cb4bc3be5; user_device_id_timestamp=1693995081802; Hm_up_d4a0e7c3cd16eb58a65472f40e7ee543=%7B%22version%22%3A%7B%22value%22%3A%222.0.0%22%2C%22scope%22%3A1%7D%2C%22has_plugin%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%7D; sid=" + sid

    materialsId, materialsTitle, materialsFormat = getMaterialsInfo(link, pinid, cookie_request)
    if materialsId != "":
        preDownload = getHuabanPreDownload(link, materialsId, cookie_request)
        #print(preDownload)
        if 'vips' in preDownload and len(preDownload['vips']) > 0:
            #if preDownload['rights'][0]['inspect']['left'] > 0:
            rs = getHuabanDownload(link, pinid, materialsId, materialsTitle, materialsFormat, preDownload, cookie_request)
            #else:
            #    print("Left Download = 0")
            return rs
        else:  
            logging.error(f"Process: getHuabanPreDownload error")
            return {'result': 'error', 'message': 'getHuabanPreDownload error'}
    else:
        logging.error(f"Process: getMaterialsInfo error")
        return {'result': 'error', 'message': 'getMaterialsInfo error'}

@app.route('/getHuabanPsd', methods=['POST'])
def get_huaban_psd():
    
    data = request.get_json()
    link = data['link'] 
    id = data['id']

    if 'x-csrf-token' not in data and data['x-csrf-token'] == 'vngetlink2023' and (link == '' or id == ''):
        return jsonify({'result': 'error', 'message': 'Authentication is required'}), 200
    
    rsData = getHuabanPSDAPI(link, id)
    
    return jsonify(rsData), 200

if __name__ == '__main__':
    app.run(debug=True)
