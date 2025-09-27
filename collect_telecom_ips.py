import requests
from bs4 import BeautifulSoup
import re

# 目标URL列表
urls = [
    'https://ip.164746.xyz/',  
    'https://www.wetest.vip/page/cloudflare/address_v4.html',
]

# IP 匹配正则
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

telecom_ips = []

# 获取 https://ip.164746.xyz/ 的 IP
try:
    response = requests.get(urls[0], timeout=8)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
except Exception:
    soup = None

if soup:
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 1:
            continue
        ip_cell = cells[0].get_text(strip=True)
        ip_matches = re.findall(ip_pattern, ip_cell)
        telecom_ips.extend(ip_matches)

# 获取 https://www.wetest.vip/page/cloudflare/address_v4.html 的电信IP
for url in urls[1:]:
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception:
        continue

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
                telecom_ips.extend(ip_matches)

# 写入文件，保持网页顺序 —— 改为写 addressesapi.txt，格式：IP#官方优选（不带端口）
if telecom_ips:
    with open('addressesapi.txt', 'w', encoding='utf-8') as f:
        for ip in telecom_ips:
            f.write(f"{ip}#官方优选\n")
