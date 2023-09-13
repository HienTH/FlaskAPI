import re
import requests


url = 'https://www.freepik.com/xhr/user/last-failed-payment'
link = "https://www.freepik.com/premium-video/focused-person-works-studies-laptop-computer-balcony-city_387505"

grtoken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5MGFkMTE4YTk0MGFkYzlmMmY1Mzc2YjM1MjkyZmVkZThjMmQwZWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTElOSyBHRVQiLCJwaWN0dXJlIjoiaHR0cHM6Ly9hdmF0YXIuY2RucGsubmV0L2RlZmF1bHRfMDgucG5nIiwiYWNjb3VudHNfdXNlcl9pZCI6OTk5Nzk1OTEsInNjb3BlcyI6ImZyZWVwaWsvaW1hZ2VzIGZyZWVwaWsvdmlkZW9zIGZsYXRpY29uL3BuZyBmcmVlcGlrL2ltYWdlcy9wcmVtaXVtIGZyZWVwaWsvdmlkZW9zL3ByZW1pdW0gZmxhdGljb24vc3ZnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2ZjLXByb2ZpbGUtcHJvLXJldjEiLCJhdWQiOiJmYy1wcm9maWxlLXByby1yZXYxIiwiYXV0aF90aW1lIjoxNjk0MDg5MDE5LCJ1c2VyX2lkIjoiM1k2SEJyWGlxRmRjcHZzMExYQmd5UkVWNjJoMiIsInN1YiI6IjNZNkhCclhpcUZkY3B2czBMWEJneVJFVjYyaDIiLCJpYXQiOjE2OTQ1NzY1ODQsImV4cCI6MTY5NDU4MDE4NCwiZW1haWwiOiJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMDQ4NDQ4ODg2MzEwNjUzNDM2NCJdLCJlbWFpbCI6WyJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.h-ek6X7ZrDhN1IjSrPF0z_iuhoAxWFNiAM0pb3D0tiotqhNnfMQX7zJKS8tHrcC8JyzbGh4cDshLYXDGUOUg3Cclcf5vrwCQxBgXcPLo8IFtObOTblDPGOeCp27a1h0xXDjTYbKXp8qIS-sWJ96O9Q7V6g0H30J-JQrstd3MAFh-WZjMsBfEec5G0LDfvHDl3PXrOB_5PTlnOwtYun_4E12HoXiAWaHjeAvkOVftdeE1U4ei8hSZlOtoVJGUxgp5xClQrbIS4k2HEq2hDPoOQP5mNm4dP6SeGfA328V-w84XqaH2BfJ29SeY6swwSfrTveNpvVq9CvtkU7H4adnD2A"
#grtoken = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjE5MGFkMTE4YTk0MGFkYzlmMmY1Mzc2YjM1MjkyZmVkZThjMmQwZWUiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiTElOSyBHRVQiLCJwaWN0dXJlIjoiaHR0cHM6Ly9hdmF0YXIuY2RucGsubmV0L2RlZmF1bHRfMDgucG5nIiwiYWNjb3VudHNfdXNlcl9pZCI6OTk5Nzk1OTEsInNjb3BlcyI6ImZyZWVwaWsvaW1hZ2VzIGZyZWVwaWsvdmlkZW9zIGZsYXRpY29uL3BuZyBmcmVlcGlrL2ltYWdlcy9wcmVtaXVtIGZyZWVwaWsvdmlkZW9zL3ByZW1pdW0gZmxhdGljb24vc3ZnIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2ZjLXByb2ZpbGUtcHJvLXJldjEiLCJhdWQiOiJmYy1wcm9maWxlLXByby1yZXYxIiwiYXV0aF90aW1lIjoxNjk0MDg5MDE5LCJ1c2VyX2lkIjoiM1k2SEJyWGlxRmRjcHZzMExYQmd5UkVWNjJoMiIsInN1YiI6IjNZNkhCclhpcUZkY3B2czBMWEJneVJFVjYyaDIiLCJpYXQiOjE2OTQ1NzY1ODQsImV4cCI6MTY5NDU4MDE4NCwiZW1haWwiOiJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiZmlyZWJhc2UiOnsiaWRlbnRpdGllcyI6eyJnb29nbGUuY29tIjpbIjExMDQ4NDQ4ODg2MzEwNjUzNDM2NCJdLCJlbWFpbCI6WyJ2aWV0bmFtZ2V0bGlua0BnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJjdXN0b20ifX0.h-ek6X7ZrDhN1IjSrPF0z_iuhoAxWFNiAM0pb3D0tiotqhNnfMQX7zJKS8tHrcC8JyzbGh4cDshLYXDGUOUg3Cclcf5vrwCQxBgXcPLo8IFtObOTblDPGOeCp27a1h0xXDjTYbKXp8qIS-sWJ96O9Q7V6g0H30J-JQrstd3MAFh-WZjMsBfEec5G0LDfvHDl3PXrOB_5PTlnOwtYun_4E12HoXiAWaHjeAvkOVftdeE1U4ei8hSZlOtoVJGUxgp5xClQrbIS4k2HEq2hDPoOQP5mNm4dP6SeGfA328V-w84XqaH2BfJ29SeY6swwSfrTveNpvVq9CvtkU7H4adnD2A"
cookie_request = "_fcid=FC.d616a023-cdd0-7789-2741-bf433ed66354; _tt_enable_cookie=1; _pin_unauth=dWlkPU1tTXpNREV3WkdZdE5HRTFaQzAwTUdGakxXSmxZemt0TUROalpURTVOamsyT1RKbA; OptanonAlertBoxClosed=2023-09-05T12:40:31.980Z; CONTRIBUTOR_FR_REFRESH=AMf-vBwv36u7ectvZKBFnZN0yAh_2dDI3A_4QAaN9X9-A8IG10sImeK2nqHxaonjHuSw_cWWSE0w5ENHvOaWdyy1wW_1wzPfnsMPv000s11vTC8kx8KAzF5IAq-r0qI_iIaMG3sXkUGMooMz7XYccVO8oiB7N0eg8w5o4s5we6FOBW2EbQVupc6Wl1viFMaTo6UpLJM556W4; ads-tag=b; _lr_geo_location_state=HN; _lr_geo_location=VN; g_state={'i_l':1,'i_p':1694096145670}; GR_REFRESH=AMf-vBy3TC0-E4Mcqn9pEhug14AhRTM-hH-ZhELeKj31zsm49Xj9AI1QPVZOfIFjpBR6goNuh3cdDZ0UHiPN_c0KTRtZEv4pQFsHkXqKwm4YYZlGcbIzE-OK0hS9-klOKu9CcVo2vxF52ft7ssxFc3K5-RTNT8lPWidlgQOYQ4eqdm6qDKsztCKVn8IbEUzuFW2MiqxvXBfh; GRID=99979591; ol-OL_Tracking_ID=99979591; G_ENABLED_IDPS=google; notify--autopromo-coupon=1; GR_TOKEN=" + grtoken + "; csrf_freepik=" + "36eb10131ef669b4c19f06d71ee7e5d4" + "; autopromo-visit={'p_ud':1694106180154,'p_vt':16}; ol-OL_LIB_INSTALL_TIME=1694112912683; refmodal=" + link

#cookie_request = "_fcid=FC.d616a023-cdd0-7789-2741-bf433ed66354; _tt_enable_cookie=1; _pin_unauth=dWlkPU1tTXpNREV3WkdZdE5HRTFaQzAwTUdGakxXSmxZemt0TUROalpURTVOamsyT1RKbA; OptanonAlertBoxClosed=2023-09-05T12:40:31.980Z; CONTRIBUTOR_FR_REFRESH=AMf-vBwv36u7ectvZKBFnZN0yAh_2dDI3A_4QAaN9X9-A8IG10sImeK2nqHxaonjHuSw_cWWSE0w5ENHvOaWdyy1wW_1wzPfnsMPv000s11vTC8kx8KAzF5IAq-r0qI_iIaMG3sXkUGMooMz7XYccVO8oiB7N0eg8w5o4s5we6FOBW2EbQVupc6Wl1viFMaTo6UpLJM556W4; ol-OL_Tracking_ID=99979591; _fc=FC.acd4c88c-cb15-c3ca-53d2-702001c0a75a; GR_TOKEN=" + grtoken + "; notify--autopromo-coupon=1; _lr_geo_location_state=HN; _lr_geo_location=VN; GR_REFRESH=AMf-vByDgYYxQqE7C3FVVhMJNzNVAJhwzCnXg4Y00ATMY_Ta7yiAWy5iAMCkrGmmPrZzeBCSQ7ViaBcx6zuMq_duDlYinWZXfQ0QFDi0nmexMmIIZF3BGd7jyf5zOPguzIXK_qJSoaPcljJSWdntm0OXtoM8iqbrZ44-raFcoX_GsF9d9rkG9TYc6MpS-6hAUvV6rEKoTFfF; GRID=99979591; ol-OL_APP_CLEAN_INSTALL_TIME=1694527775664; ol-OL_LIB_INSTALL_TIME=1694527775664; autopromo-visit={'p_ud':1694106180154,'p_vt':45}; refmodal=https://www.freepik.com/premium-photo/young-asian-high-school-girl-blue-background_24415781.htm#query=student&position=1&from_view=search&track=sph;"

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

timeout = 5

response = requests.get(url, headers=headers, timeout=timeout)

# Get the "Set-Cookie" header value
set_cookie_header = response.headers.get('Set-Cookie', '')

# Use regular expressions to extract the value of the GR_TOKEN cookie
match = re.search(r'GR_TOKEN=([^;]+)', set_cookie_header)

if match:
    gr_token = match.group(1)
    print(f'GR_TOKEN: {gr_token}')
else:
    print('GR_TOKEN not found in the Set-Cookie header')

# Iterate through and print all response headers
#for key, value in response.headers.items():
#    if key == "set-cookie":
#        print(f'{key}: {value}')
