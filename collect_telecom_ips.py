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
        if len(cells) < 3:  # 至少有运营商、IP、延迟
            continue

        carrier = cells[0].get_text(strip=True)
        ip_cell = cells[1].get_text(strip=True)
        latency_text = cells[2].get_text(strip=True)  # 网页里的“往返延迟”列

        if '电信' in carrier:
            ip_matches = re.findall(ip_pattern, ip_cell)
            try:
                # 尝试将“ms”去除并转为浮动数值
                latency = float(latency_text.replace("ms", "").strip())
            except ValueError:
                latency = float('inf')  # 无法解析时设为最大值
            for ip in ip_matches:
                telecom_ips.append((ip, latency))

# 按网页中的“往返延迟”进行排序
telecom_ips_sorted = sorted(telecom_ips, key=lambda x: x[1])

# 写入文件
if telecom_ips_sorted:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip, _ in telecom_ips_sorted:
            f.write(f"{ip}:443#官方优选\n")
    print(f'已保存 {len(telecom_ips_sorted)} 个电信IP到 ip.txt (按往返延迟排序)')
else:
    print('未找到电信IP，保留现有 ip.txt')
