import requests
from bs4 import BeautifulSoup
import re
import os

# 目标 URL
url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 正则表达式匹配 IP 地址，不带端口
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 删除旧文件
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 存储唯一 IP
unique_ips = []

try:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        html_content = response.text
        ip_matches = re.findall(ip_pattern, html_content)
        # 只保留电信 IP，前 5 个
        for ip in ip_matches:
            if '电信' in html_content and ip not in unique_ips:
                unique_ips.append(ip)
            if len(unique_ips) >= 5:
                break
except requests.exceptions.RequestException as e:
    print(f'请求失败: {e}')

# 写入文件，备注“狮城”
if unique_ips:
    with open('ip.txt', 'w') as f:
        for ip in unique_ips:
            f.write(f'{ip} # 狮城\n')
    print(f'已保存 {len(unique_ips)} 个电信 IP 到 ip.txt（备注“狮城”）')
else:
    print('未找到有效的电信 IP')
