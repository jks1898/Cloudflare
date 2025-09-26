import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL
url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 匹配IP的正则
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 如果 ip.txt 存在就删除
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 存储去重的电信IP
telecom_ips = []

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('tr')
    
    for row in rows:
        if len(telecom_ips) >= 5:
            break
        cells = row.find_all('td')
        if len(cells) >= 2:
            carrier = cells[0].get_text(strip=True)
            ip_cell = cells[1].get_text(strip=True)
            ip_match = re.search(ip_pattern, ip_cell)
            if ip_match and '电信' in carrier:
                ip = ip_match.group(0)
                if ip not in telecom_ips:
                    telecom_ips.append(ip)

except Exception as e:
    print(f'获取或解析网页失败: {e}')

# 只保留 443 端口
if telecom_ips:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip in telecom_ips:
            f.write(f"{ip}:443#狮城\n")
    print(f'已保存 {len(telecom_ips)} 个电信IP，每个仅写入 443 端口到 ip.txt')
else:
    print('未找到有效的电信IP')
