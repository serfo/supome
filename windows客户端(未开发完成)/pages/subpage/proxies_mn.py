import configparser
from bs4 import BeautifulSoup
import requests



def get_proxies():
    config = configparser.ConfigParser()
    file = '../../config/login_info.ini'
    config.read(file, encoding='utf-8')
    cookies = config['login'].get('cookies', '')
    params = {
        'page': "panel",
        'module': "proxies"
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
    # 使用BeautifulSoup解析HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 查找表格体
    table_body = soup.find('tbody')


    tunnel_list = []

    # 遍历表格中的每一行
    for row in table_body.find_all('tr'):
        columns = row.find_all('td')
        tunnel_info = {
            'ID': columns[0].text.strip(),
            '隧道名称': columns[1].text.strip(),
            '服务器节点': columns[4].text.strip(),
            '主机名访问': columns[5].find('a').get('href') if columns[5].find('a') else 'N/A',
            '绑定域名 / 远程端口': columns[3].text.strip(),
            '隧道类型': columns[2].text.strip(),
        }
        tunnel_list.append(tunnel_info)

    return tunnel_list