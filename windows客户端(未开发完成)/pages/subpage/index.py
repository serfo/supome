import configparser
import requests
from bs4 import BeautifulSoup


def get_index():
    config = configparser.ConfigParser()
    file = '../../config/login_info.ini'
    config.read(file, encoding='utf-8')
    cookies = config['login'].get('cookies', '')
    params = {
        'page': "panel",
        'module': "profile"
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

    response = requests.get("http://www.supo.me/", params=params, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    account_info_table = soup.find('table', class_='download')
    account_info = {}
    for row in account_info_table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            account_info[key] = value

    # 提取映射信息
    mapping_info_table = soup.find_all('table', class_='download')[1]
    mapping_info = {}
    for row in mapping_info_table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 1:
            key = cells[0].get_text(strip=True)
            value = cells[1].get_text(strip=True)
            mapping_info[key] = value

    # 假设访问密钥（token）是在account_info中的一个键值对
    token = account_info.get('访问密钥')  # 这里的'访问密钥'需要根据实际页面内容来确定
    if token:
        update_config_file(file, token)

    return account_info, mapping_info


def update_config_file(file_path, token):
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')
    if not config.has_section('token'):
        config.add_section('token')
    config.set('token', 'token', token)

    with open(file_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)


def to_markdown(account_info, mapping_info):
    markdown_text = "## 账户信息\n"
    for key, value in account_info.items():
        markdown_text += f"* **{key}**: {value}\n"

    markdown_text += "\n## 映射信息\n"
    for key, value in mapping_info.items():
        markdown_text += f"* **{key}**: {value}\n"
    return markdown_text


def get_markdown_content():
    account_info, mapping_info = get_index()
    return to_markdown(account_info, mapping_info)

