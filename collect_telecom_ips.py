import requests
from bs4 import BeautifulSoup
import re
import os

# 目标 URL
url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 正则匹配 IP
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 删除旧文件
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

telecom_ips = []

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 遍历表格，找到电信 IP
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            carrier = cells[0].get_text(strip=True)
            ip_cell = cells[1].get_text(strip=True)
            ip_match = re.search(ip_pattern, ip_cell)
            if ip_match and '电信' in carrier:
                telecom_ips.append(ip_match.group(0))
                if len(telecom_ips) >= 5:
                    break

except Exception as e:
    print(f"拉取或解析失败: {e}")

# 去重并按数字排序
unique_sorted_ips = sorted(set(telecom_ips), key=lambda ip: [int(part) for part in ip.split('.')])

# 写入 ip.txt，每个 IP 使用 443 端口，备注“狮城”
if unique_sorted_ips:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip in unique_sorted_ips:
            f.write(f"{ip}:443#狮城\n")
    print(f"已保存 {len(unique_sorted_ips)} 个电信 IP 到 ip.txt")
else:
    print("未找到电信 IP")
