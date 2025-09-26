import requests
from bs4 import BeautifulSoup
import re

# 目标URL
url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 匹配IP的正则
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# 存储 (IP, 网页延迟)
telecom_ips = []

try:
    response = requests.get(url, timeout=8)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

except Exception as e:
    print(f'获取或解析网页失败: {e}')
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
                # 直接取网页显示的延迟数字
                try:
                    latency = float(re.sub(r'[^0-9.]', '', latency_text))
                except ValueError:
                    latency = float('inf')  # 出错时放到最后
                telecom_ips.append((ip, latency))

# 按网页给出的延迟升序排序
telecom_ips_sorted = sorted(telecom_ips, key=lambda x: x[1])

if telecom_ips_sorted:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip, latency in telecom_ips_sorted:
            f.write(f"{ip}:443#官方优选\n")
    print(f'已保存 {len(telecom_ips_sorted)} 个电信IP到 ip.txt (按网页延迟排序)')
else:
    print('未找到有效的电信IP，保留现有的 ip.txt')
