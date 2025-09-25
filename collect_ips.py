import requests
from bs4 import BeautifulSoup
import re
import os

# 目标URL列表
urls = [
    'https://www.wetest.vip/page/cloudflare/address_v4.html'
]

# 正则表达式用于匹配IP地址
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 检查ip.txt文件是否存在,如果存在则删除它
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

# 使用集合存储IP地址实现自动去重
unique_ips = set()

for url in urls:
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            html_content = response.text
            ip_matches = re.findall(ip_pattern, html_content, re.IGNORECASE)
            unique_ips.update(ip_matches)
    except requests.exceptions.RequestException as e:
        print(f'请求 {url} 失败: {e}')
        continue

if unique_ips:
    sorted_ips = sorted(unique_ips, key=lambda ip: [int(part) for part in ip.split('.')])

    tsl_ports = ["443", "8443", "2053", "2083", "2087", "2096"]

    # 解析网页获取运营商信息
    telecom_ip = None
    try:
        response = requests.get(urls[0], timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            rows = soup.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    carrier = cells[0].get_text().strip()
                    ip_cell = cells[1].get_text().strip()
                    ip_match = re.search(ip_pattern, ip_cell)
                    if ip_match and '电信' in carrier:
                        telecom_ip = ip_match.group(0)
                        break

        # 如果没有解析到电信IP，使用前三个IP中的第三个
        if not telecom_ip and len(sorted_ips) > 2:
            telecom_ip = sorted_ips[2]
    except Exception as e:
        print(f'解析运营商信息失败: {e}')
        if len(sorted_ips) > 2:
            telecom_ip = sorted_ips[2]

    # 为电信IP添加端口和备注
    result = []
    if telecom_ip:
        for port in tsl_ports:
            result.append(f"{telecom_ip}:{port}#官方优选")

    # 写入ip.txt
    with open('ip.txt', 'w', encoding='utf-8') as file:
        for line in result:
            file.write(line + '\n')

    print(f'已保存 {len(result)} 条电信IP到ip.txt文件。')
    print(f'电信IP: {telecom_ip}')
else:
    print('未找到有效的IP地址。')
