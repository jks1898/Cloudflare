import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL
url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 匹配IP的正则
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 存储 (IP, 峰值速度)
telecom_ips = []

try:
    response = requests.get(url, timeout=8)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')

    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 3:  # 假设第3列是峰值速度
            carrier = cells[0].get_text(strip=True)
            ip_cell = cells[1].get_text(strip=True)
            speed_text = cells[2].get_text(strip=True)

            ip_match = re.search(ip_pattern, ip_cell)
            if ip_match and '电信' in carrier:
                ip = ip_match.group(0)

                # 解析速度
                try:
                    speed = float(re.sub(r'[^0-9.]', '', speed_text))
                except:
                    speed = 0.0

                telecom_ips.append((ip, speed))

except Exception as e:
    print(f'获取或解析网页失败: {e}')

# 排序，取前 5
telecom_ips = sorted(telecom_ips, key=lambda x: x[1], reverse=True)[:5]

# 只有找到电信 IP 才写入，否则保留旧文件
if telecom_ips:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip, speed in telecom_ips:
            f.write(f"{ip}:443#狮城\n")
    print(f'已保存 {len(telecom_ips)} 个电信IP到 ip.txt (按峰值速度排序)')
else:
    print('未找到有效的电信IP，保留现有的 ip.txt')
