import requests
import json

def fetch_resources(url, staff_name: str=''):
    req_params = {}
    if staff_name:
        req_params['roles__staffs__name'] = staff_name
    
    res = requests.get(url, params=req_params)
    return json.loads(res.text)

def get_all_movies(url):
    next_url = url
    while True:
        res = fetch_resources(next_url)
        print([movie['name'] for movie in res['results']])
        next_url = res['next']
        if not next_url:
            break

def get_movie_by_staff(url):
    next_url = url
    while True:
        staff_name = input('スタッフ名を入力してください')
        res = fetch_resources(next_url, staff_name)
        print([movie['name'] for movie in res['results']])
        next_url = res['next']
        if not next_url:
            break

def login_api(login_url, username, password):
    res = requests.post(login_url, data={
        'username': username,
        'password': password
    })
    print(res.text)
    return res.text

def get_login_token(login_url, username, password):
    res = requests.post(login_url, data={
        'username': username,
        'password': password
    })
    return res.json()['token']

def post_comment(url, token, star: int, comment: str):
    res = requests.post(
        url,
        data={
            'star': star,
            'comment': comment
        },
        headers={
            'Authorization': f'Token {token}'  # 認証トークン付与
        }
    )
    print(res.text)


url = 'http://127.0.0.1:8000/api/movies/'
get_all_movies(url)

login_url = 'http://127.0.0.1:8000/api/login/'
login_api(login_url, 'user', '12345678')

login_token_url = 'http://127.0.0.1:8000/api_token_auth/'
token = get_login_token(login_token_url, 'user', '12345678')

add_comment_url = 'http://127.0.0.1:8000/api/movies/4/comments/'
post_comment(add_comment_url, token=token, star=5, comment='良い映画')
