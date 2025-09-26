import requests
from bs4 import BeautifulSoup
import re

# 目标URL
url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# IP 匹配正则
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

telecom_ips = []

try:
    response = requests.get(url, timeout=8)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
except Exception as e:
    print(f'获取网页失败: {e}')
    soup = None

if soup:
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 2:
            continue

        carrier = cells[0].get_text(strip=True)
        ip_cell = cells[1].get_text(strip=True)

        if '电信' in carrier:
            ip_matches = re.findall(ip_pattern, ip_cell)
            for ip in ip_matches:
                telecom_ips.append(ip)
                print(f"发现电信IP: {ip}")  # 调试输出

# 如果找到了电信IP才写入文件
if telecom_ips:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip in telecom_ips:
            f.write(f"{ip}:443#官方优选\n")
    print(f'已保存 {len(telecom_ips)} 个电信IP到 ip.txt')
else:
    print('未找到电信IP，保留现有 ip.txt')
