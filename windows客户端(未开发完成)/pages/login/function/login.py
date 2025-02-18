import requests
# from requests.cookies import cookiejar_from_dict
from bs4 import BeautifulSoup

url = "http://www.supo.me/"

def login_get_cookies(username,password):
    params = {
      'action': "login",
      'page': "login"
    }

    payload = {
      'g-recaptcha-response': "<reCAPTCHA_RESPONSE>",
      'username': username,
      'password': password,
    }
    response = requests.post(url, params=params, data=payload)
    cookies_str = response.cookies
    cookies_dict = cookies_str.get_dict()
    cookies = '; '.join([f'{name}={value}' for name, value in cookies_dict.items()])
    return cookies


def login_status(cookies):
    url = "http://www.supo.me/"  # 确保URL是正确的
    params = {
        'page': "panel"
    }

    headers = {
        'Host': "www.supo.me",
        'Upgrade-Insecure-Requests': "1",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        'Referer': "http://www.supo.me/?action=login&page=login",
        'Accept-Encoding': "gzip, deflate",
        'Accept-Language': "zh-CN,zh;q=0.9,en;q=0.8",
        'Cookie': cookies
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        # 查找用户名元素
        username_element = soup.find('a', class_='d-block')
        user = username_element.text.strip() if username_element else None

        # 查找邮箱元素
        email_element = soup.find('td', text='注册邮箱')
        email = email_element.find_next_sibling('td').text.strip() if email_element and email_element.find_next_sibling(
            'td') else None

        return user, email
    except Exception as e:
        pass