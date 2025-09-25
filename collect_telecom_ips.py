import requests
from bs4 import BeautifulSoup
import re
import os

url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'
ip_file = 'ip.txt'

# 删除旧文件
if os.path.exists(ip_file):
    os.remove(ip_file)

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # 正则匹配 IPv4
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    telecom_ips = []

    # 遍历表格行，找电信 IP
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            carrier = cells[0].get_text().strip()
            ip_cell = cells[1].get_text().strip()
            if '电信' in carrier:
                ip_match = re.search(ip_pattern, ip_cell)
                if ip_match:
                    telecom_ips.append(ip_match.group(0))
        if len(telecom_ips) >= 5:
            break

    if telecom_ips:
        with open(ip_file, 'w') as f:
            for ip in telecom_ips:
                f.write(f"{ip}:443#狮城\n")
        print(f"已保存 {len(telecom_ips)} 个电信 IP 到 {ip_file}。")
    else:
        print("未找到电信 IP。")

except requests.RequestException as e:
    print(f"请求失败: {e}")
