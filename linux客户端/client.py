import subprocess
import os
import requests
import json
import sys

url = 'http://api.supo.me:6001/dash_app' #服务器后端
logged_in_data = None  # 全局变量存储登录信息
login_info = None  # 存储登录信息

def login():
    global logged_in_data, login_info
    if logged_in_data is None or login_info is None:
        max_attempts = 5  # 设定最大尝试次数
        attempts = 0  # 初始化尝试计数器

        while attempts < max_attempts:
            username = input("输入用户名: ")
            password = input("输入密码: ")
            info = {'username': username, 'password': password}
            req = requests.post(url, json=info)

            # 检查返回的状态
            if req.status_code == 200:  # 登录请求成功
                logged_in_data = req.json(), info
                login_info = info
                if logged_in_data[0].get('op'):
                    print("登录成功")
                    return logged_in_data
                else:
                    print(logged_in_data[0].get('remark'))  # 显示错误信息
            else:
                print("请求失败，请稍后再试。")

            attempts += 1  # 递增尝试计数器
            print(f"剩余尝试次数: {max_attempts - attempts}")

        print("达到最大尝试次数，程序退出。")
        sys.exit(1)  # 退出程序

    return logged_in_data

def find_frpc():
    # 方法1: 在 PATH 中查找 frpc
    for path in os.environ["PATH"].split(os.pathsep):
        frpc_path = os.path.join(path, "frpc")
        if os.path.isfile(frpc_path) and os.access(frpc_path, os.X_OK):
            return "已安装"

    # 方法2: 使用 `find` 命令在整个文件系统中查找 frpc
    find_cmd = "find / -name frpc -type f -executable 2>/dev/null"
    try:
        process = subprocess.Popen(find_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stdout.strip():
            return "已安装"
    except Exception as e:
        return "未知状态: " + str(e)

    # 方法3: 检查是否由 systemd 管理
    systemctl_cmd = "systemctl list-units --type=service | grep -q frpc && echo 0 || echo 1"
    try:
        process = subprocess.Popen(systemctl_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if stdout.strip() == "0":
            return "已安装"
    except Exception as e:
        return "未知状态: " + str(e)

    return "未安装"

def get_nodes(data, login_info):
    if not data or not login_info:
        return [], {}, []

    # 服务器节点配置文件节点信息
    nodes = data.get('config', {}).get('nodes', [])
    server_config = [
        f'''
[common]
server_addr = {node['ip']}
server_port = {node['port']}
tcp_mux = true
protocol = tcp
user = {data['config']['token']['token']}
token = {node.get('token')}
dns_server = 114.114.114.114
''' for node in nodes
    ]

    # 用户隧道配置文件节点信息
    proxies = data.get('config', {}).get('proxies', [])
    proxies_config = {}  # 用于存储每个节点下的代理配置

    for proxy in proxies:
        # 查找匹配的节点
        matching_node = next((node for node in nodes if node['id'] == proxy.get('node')), None)

        # 如果不是此节点的忽略
        if not matching_node or proxy.get('proxy_type', '') != 'tcp':
            continue

        # 防止出现 Bug
        local_ip = proxy.get('local_ip', '127.0.0.1')
        local_port = proxy.get('local_port', '80')

        # 隧道的基本信息
        proxy_name = proxy.get('proxy_name', '')
        config_str = f'''
[{proxy_name}]
privilege_mode = true
type = {proxy.get('proxy_type', '')}
local_ip = {local_ip}
local_port = {local_port}
'''

        if proxy.get('proxy_type', '') in ['http', 'https']:
            # HTTP / HTTPS
            domain = proxy.get('domain', '')
            locations = proxy.get('locations', '')
            host_header_rewrite = proxy.get('host_header_rewrite', '')
            header_x_from_where = proxy.get('header_x_from_where', '')

            config_str += f'custom_domains = {domain}\n'
            config_str += f'locations = {locations}\n' if locations else ''
            config_str += f'host_header_rewrite = {host_header_rewrite}\n' if host_header_rewrite else ''
            config_str += f'header_x_from_where = {header_x_from_where}\n' if header_x_from_where else ''
        else:
            # TCP / UDP / XTCP / STCP
            remote_port = proxy.get('remote_port', '')
            sk = proxy.get('sk', '')

            config_str += f'remote_port = {remote_port}\n' if remote_port else ''
            config_str += f'sk = {sk}\n' if sk else ''

        # 压缩和加密
        use_encryption = proxy.get('use_encryption', '')
        use_compression = proxy.get('use_compression', '')

        config_str += f'use_encryption = {use_encryption}\n' if use_encryption else ''
        config_str += f'use_compression = {use_compression}\n' if use_compression else ''
        config_str += '\n'

        if matching_node['id'] not in proxies_config:
            proxies_config[matching_node['id']] = {}
        proxies_config[matching_node['id']][proxy_name] = {
            "proxies": config_str,
            "proxy_id": proxy.get('id', '')
        }
    return server_config, proxies_config, nodes


def Selection_Panel(server_config, proxies_config):
    def display_node_info():
        node_info = '\n'.join([
            f'当前在节点 \033[1;36m{node["id"]}\033[0m  :  {node["name"]} \n'
            + '\n'.join(
                [f'    \033[1;33m隧道名称：{proxy}\033[0m, \033[1;32m隧道ID：{proxy_info["proxy_id"]}\033[0m'
                 for proxy, proxy_info in proxies_config.get(node['id'], {}).items()])
            for node in nodes
        ])
        print("-" * 46, "隧道信息", "-" * 46)
        print(node_info)
        print("-" * 100)

    while True:
        try:
            print("\n请选择要进行的操作：")
            print("1. 刷新节点信息")
            print("2. 部署隧道到本机")
            print("3. 管理内网穿透服务")
            print("4. 退出程序")
            choice = input("请输入选项（1/2/3/4）: ")

            if choice == '1':
                data, _ = login()  # 重新获取数据
                server_config, proxies_config, nodes = get_nodes(data, login_info)
                display_node_info()
            elif choice == '2':
                deploy_proxy_panel(server_config, proxies_config)
            elif choice == '3':
                frpc_mange()
            elif choice == '4':
                print("感谢使用，再见！")
                sys.exit(0)
            else:
                print("无效的选择，请重新输入！")

        except KeyboardInterrupt:
            print("\n检测到 Ctrl+C，正在退出程序...")
            sys.exit(0)
        except Exception as e:
            print(f"发生错误: {e}, 请重试。")



def deploy_proxy_panel(server_config, proxies_config):
    status = find_frpc()
    if status == "未安装":
        print("frpc 未安装，请先安装 frpc。")
        print("\033[33m请在命令行安装: curl -L supo.me/frpc.sh -o frpc.sh && chmod +x frpc.sh && ./frpc.sh\033[0m")
        return
    if not proxies_config:
        print("没有可用的节点，请刷新节点信息。")
        return

    # 显示所有节点供用户选择
    print("\n请选择一个节点（输入节点ID）：")
    for idx, node_id in enumerate(proxies_config.keys(), start=1):
        print(f"{idx}. 节点 {node_id}")

    choice = input("请输入节点ID（输入0返回上一级）: ")
    if choice.isdigit():
        choice = int(choice)
        if choice == 0:
            return  # 返回上一级
        if 0 < choice <= len(proxies_config):
            selected_node_id = list(proxies_config.keys())[choice - 1]
            selected_node_proxies = proxies_config[selected_node_id]

            # 获取所选节点的配置索引
            selected_node_index = int(selected_node_id) - 1  # 转换为索引
            if selected_node_index < 0 or selected_node_index >= len(server_config):
                print("未找到对应的节点配置。")
                return
            # 获取选定节点的所有代理ID
            proxy_ids = [str(proxy_info['proxy_id']) for proxy_info in selected_node_proxies.values()]

            # 选择隧道ID
            while True:
                print("\n请选择要部署的隧道ID（输入ID，以逗号分隔，输入0返回上一级）：")
                for idx, (proxy_name, proxy_info) in enumerate(selected_node_proxies.items(), start=1):
                    print(proxy_info)
                    print(f"{idx}. 隧道名称：{proxy_name}，隧道ID：{proxy_info['proxy_id']}")
                    # print(f"{idx}. 隧道名称：{proxy_name}，隧道ID：{proxy_info['proxy_id']}，本地端口:{proxy_info['local_port']},远程端口:{proxy_info['remote_port']}")

                choice = input("请输入隧道ID（用逗号分隔）: ").strip()

                if choice == '0':
                    return  # 返回上一级
                else:
                    selected_proxy_ids = [proxy_id.strip() for proxy_id in choice.split(',')]
                    invalid_ids = [proxy_id for proxy_id in selected_proxy_ids if proxy_id not in proxy_ids]

                    if invalid_ids:
                        print(f"无效的隧道ID: {', '.join(invalid_ids)}，请重新输入。")
                    else:
                        # 整合配置文件
                        config_content = ""
                        config_content += server_config[selected_node_index] + "\n"

                        for proxy_name, proxy_info in selected_node_proxies.items():
                            if str(proxy_info['proxy_id']) in selected_proxy_ids:
                                config_content += proxy_info['proxies'] + "\n"

                        if config_content.strip():
                            # 让用户选择保存路径
                            file_path = input("请输入保存路径（回车使用默认 /frpc/frpc.ini）: ")
                            if not file_path.strip():
                                file_path = '/frpc/frpc.ini'

                            # 保存到指定路径
                            with open(file_path, 'w') as file:
                                file.write(config_content)

                            print(f"配置已保存至 {file_path} 文件，使用systemctl start frpc开启服务")
                        else:
                            print("配置内容为空，无法写入文件。")
                        break

        else:
            print("无效的选择，请重新输入！")
            deploy_proxy_panel(server_config, proxies_config)
    else:
        print("输入错误，请输入数字！")
        deploy_proxy_panel(server_config, proxies_config)








def frpc_mange():
    status = find_frpc()
    if status == "未安装":
        print("frpc 未安装，请先安装 frpc。")
        print("\033[33m请在命令行安装: curl -L supo.me/frpc.sh -o frpc.sh && chmod +x frpc.sh && ./frpc.sh\033[0m")
        return

    commands = [
        ("关闭防火墙（如果使用 firewall）", "systemctl stop firewalld"),
        ("启动 frpc 服务(请先配置frpc.ini)", "systemctl start frpc"),
        ("停止 frpc 服务", "systemctl stop frpc"),
        ("设置 frpc 不开机自启", "systemctl disable frpc"),
        ("设置 frpc 开机自启", "systemctl enable frpc"),
        ("重启 frpc 服务", "systemctl restart frpc"),
        ("查看 frpc 服务状态", "systemctl status frpc")
    ]

    print("\n请选择要执行的操作：")
    for idx, (description, command) in enumerate(commands, start=1):
        print(f"{idx}. {description}")

    choice = input("请输入选项（1-7）: ")

    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= len(commands):
            description, command = commands[choice - 1]
            print(f"\n执行命令：{command}")
            try:
                process = subprocess.run(command, shell=True, check=True)
                print(f"{description} 成功。")
            except subprocess.CalledProcessError as e:
                print(f"执行命令失败：{e}")
        else:
            print("无效的选择，请重新输入！")
            frpc_mange()
    else:
        print("输入错误，请输入数字！")
        frpc_mange()


def main():
    global logged_in_data, login_info
    logged_in_data = None  # 每次运行程序时重置登录信息
    login_info = None

    while logged_in_data is None or not logged_in_data[0].get('op'):
        data, login_info = login()
        if not data.get('op'):
            print(data.get('remark'))
        else:
            print("登录成功")

    status = find_frpc()

    if status == "未安装":
        soft_install_info = "\033[33m请在命令行安装: curl -L supo.me/frpc.sh -o frpc.sh && chmod +x frpc.sh && ./frpc.sh\033[0m"
    elif status == "已安装":
        soft_install_info = "\033[36m无需再次安装\033[0m"

    # 打印软件安装状态信息
    soft_info = f'''
软件安装状态: \033[36m{status}\033[0m , {soft_install_info}
    '''

    # 调用数据库获节点信息，和隧道服务器配置文本
    server_config, proxies_config, nodes = get_nodes(data, login_info)
    node_info = '\n'.join([
        f'当前在节点 \033[1;36m{node["id"]}\033[0m  :  {node["name"]} \n'
        + '\n'.join([f'    \033[1;33m隧道名称：{proxy}\033[0m, \033[1;32m隧道ID：{proxy_info["proxy_id"]}\033[0m'
                     for proxy, proxy_info in proxies_config.get(node['id'], {}).items()])
        for node in nodes
    ])

    # 打印分割线、软件安装状态信息、节点信息以及分割线
    print("-" * 46,"软件状态","-" * 46)
    print(soft_info)
    print("-" * 46,"隧道信息","-" * 46)
    print(node_info)
    print("-" * 100)

    # 进入选择面板
    Selection_Panel(server_config, proxies_config)

def show_main():
    main()

if __name__ == "__main__":
    show_main()