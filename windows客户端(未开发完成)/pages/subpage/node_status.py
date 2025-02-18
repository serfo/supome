import os
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
import requests


def get_node_status():
    url = "http://jk.supo.me:6002/api/v1/server/details"
    params = {'id': "", 'tag': "supo"}
    headers = {'Authorization': "e8bPdcYVJpbpviG9OQ630Vfw11vT0KyE"}

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if data['code'] != 0:
        raise Exception(f"请求失败: {data['message']}")

    return data['result']


def plot_server_status(server_list):
    markdown_text = "## 服务器信息\n"
    markdown_text += "#####   -每10秒刷新\n"
    for server in server_list:
        server_name = server['name'].strip()  # 去除前后空白
        cpu = server['status']['CPU']
        net_in_speed_mb = server['status']['NetInSpeed'] / (1024 * 1024)
        net_out_speed_mb = server['status']['NetOutSpeed'] / (1024 * 1024)

        markdown_text += f"- **名称**: {server_name}\n"
        markdown_text += f"  - **CPU 使用率**: {cpu}%\n"
        markdown_text += f"  - **网络输入速度**: {net_in_speed_mb:.2f} MB/s\n"
        markdown_text += f"  - **网络输出速度**: {net_out_speed_mb:.2f} MB/s\n\n"
    return markdown_text


def get_markdown_content():
    server_list = get_node_status()
    markdown_content = plot_server_status(server_list)
    return markdown_content
