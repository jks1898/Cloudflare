import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL
url = 'https://api.uouin.com/cloudflare.html'

# 匹配IP的正则
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 存储 (IP, 延迟)
telecom_ips = []

try:
    response = requests.get(url, timeout=8)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')

    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 3:  # 假设第3列是延迟
            carrier = cells[0].get_text(strip=True)
            ip_cell = cells[1].get_text(strip=True)
            latency_text = cells[2].get_text(strip=True)

            ip_match = re.search(ip_pattern, ip_cell)
            if ip_match and '电信' in carrier:
                ip = ip_match.group(0)

                # 解析延迟
                try:
                    latency = float(re.sub(r'[^0-9.]', '', latency_text))
                except:
                    latency = float('inf')  # 解析失败当成无效

                telecom_ips.append((ip, latency))

except Exception as e:
    print(f'获取或解析网页失败: {e}')

# 排序，按延迟升序（越小越快），取前 5
telecom_ips = sorted(telecom_ips, key=lambda x: x[1])[:5]

# 只有找到电信 IP 才写入，否则保留旧文件
if telecom_ips:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip, latency in telecom_ips:
            f.write(f"{ip}:443#官方优选\n")
    print(f'已保存 {len(telecom_ips)} 个电信IP到 ip.txt (按延迟排序)')
else:
    print('未找到有效的电信IP，保留现有的 ip.txt')
