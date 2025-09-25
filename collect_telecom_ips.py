import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 发起请求
response = requests.get(url, timeout=5)
response.raise_for_status()

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(response.text, 'html.parser')

# 存储匹配的电信 IP
telecom_ips = []

# 遍历页面中所有文本块
for element in soup.stripped_strings:
    if '电信' in element:
        ip_match = re.search(ip_pattern, element)
        if ip_match:
            telecom_ips.append(ip_match.group())
    if len(telecom_ips) >= 5:
        break

# 写入 ip.txt
with open('ip.txt', 'w') as f:
    for ip in telecom_ips:
        f.write(f'{ip} # 狮城\n')

print(f'已写入 {len(telecom_ips)} 个电信 IP 到 ip.txt')
