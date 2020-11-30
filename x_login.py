import random
import re
import sys
import requests
from bs4 import BeautifulSoup


def rco_captcha(captcha_url, session=None):
    headers = {
        'referer': f'https://{host}/login',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
    }
    if session:
        image = session.get(captcha_url).content
    else:
        image = requests.get(captcha_url, headers=headers).content
    reco_info = requests.post('http://47.98.142.71:19952/captcha/v3', data=image).json()
    if reco_info['success']:
        return reco_info['message']

def login(email, passwd):
    while True:
        headers = {
            'referer': f'https://{host}/login',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'
        }
        session = requests.session()
        session.headers = headers
        login_page = session.get(f'https://{host}/login')
        soup = BeautifulSoup(login_page.content, 'html5lib')
        captcha_tag = soup.select(
            '#app > section > div > div > div > div.card.card-primary > div.card-body > form > div:nth-child(5) > div > div > span > img')[
            0]
        captcha_url = captcha_tag['src']
        captcha = rco_captcha(captcha_url, session)
        token_tag = soup.select(
            '#app > section > div > div > div > div.card.card-primary > div.card-body > form > div:nth-child(2) > input[type=hidden]:nth-child(3)')[
            0]
        token = token_tag['value']
        login_post_data = {
            'username': email,
            'password': passwd,
            '_token': token,
            'captcha': captcha,
            'remember': 1
        }
        login_info = session.post(f'https://{host}/login', data=login_post_data)
        if login_info.text.find('验证码错误') == -1:
            break
        print('验证码错误，正在重试')
    return session, login_info.text


if __name__ == "__main__":
    username = sys.argv[1]
    password = sys.argv[2]
    host = sys.argv[3]
    
    session, user_html = login(username, password)
    if not random.randint(0, 5):
        token = re.search(r"_token = '(\w*)'", user_html)[1]
        session.post(f'https://{host}/user/exchange', data={'_token': token})
