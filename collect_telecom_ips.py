import requests
from bs4 import BeautifulSoup
import re

# 目标URL列表
urls = [
    'https://ip.164746.xyz/',  # 直接获取此网址上的 IP
    'https://www.wetest.vip/page/cloudflare/address_v4.html',
]

# IP 匹配正则
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

telecom_ips = set()  # 用 set 去重

# 获取 https://ip.164746.xyz/ 的 IP
try:
    response = requests.get(urls[0], timeout=8)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
except Exception as e:
    print(f'获取网址 {urls[0]} 失败: {e}')
    soup = None

if soup:
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 1:
            continue
        ip_cell = cells[0].get_text(strip=True)  # 直接提取 IP 地址
        ip_matches = re.findall(ip_pattern, ip_cell)
        for ip in ip_matches:
            telecom_ips.add(ip)  # 直接加进 set 去重
            print(f"发现IP: {ip}")  # 调试输出

# 获取其他网址的电信IP
for url in urls[1:]:  # 从第二个网址开始抓取
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f'获取网页失败 {url}: {e}')
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
                for ip in ip_matches:
                    telecom_ips.add(ip)
                    print(f"发现电信IP: {ip}")  # 调试输出

# 如果找到了IP才写入文件
if telecom_ips:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip in telecom_ips:
            f.write(f"{ip}:443#官方优选\n")
    print(f'已保存 {len(telecom_ips)} 个IP到 ip.txt')
else:
    print('未找到IP，保留现有 ip.txt')
