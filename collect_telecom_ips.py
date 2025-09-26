import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

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
        if len(cells) < 3:
            continue

        carrier = cells[0].get_text(strip=True)
        ip_cell = cells[1].get_text(strip=True)
        latency_text = cells[2].get_text(strip=True)

        if '电信' in carrier:
            ip_match = re.search(ip_pattern, ip_cell)
            if ip_match:
                ip = ip_match.group(0)
                try:
                    # 严格按照网页显示的数值转换为浮点数
                    latency = float(latency_text)
                except ValueError:
                    # 如果无法转换，直接用一个很大的值放到最后
                    latency = float('inf')
                telecom_ips.append((ip, latency))

# 完全按照网页给出的延迟排序（从小到大）
telecom_ips_sorted = sorted(telecom_ips, key=lambda x: x[1])

if telecom_ips_sorted:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip, latency in telecom_ips_sorted:
            f.write(f"{ip}:443#官方优选\n")
    print(f'已保存 {len(telecom_ips_sorted)} 个电信IP到 ip.txt (严格按网页延迟排序)')
else:
    print('未找到有效的电信IP，保留现有的 ip.txt')
