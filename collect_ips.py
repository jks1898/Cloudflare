import requests
from bs4 import BeautifulSoup
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')

# 目标网页
URL = 'https://www.wetest.vip/page/cloudflare/address_v4.html'
IP_PATTERN = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
OUTPUT_FILE = 'ip.txt'
TSL_PORTS = ["443", "8443", "2053", "2083", "2087", "2096"]
MAX_IPS = 5  # 最多保留5个电信IP

try:
    response = requests.get(URL, timeout=5)
    response.raise_for_status()
except requests.RequestException as e:
    logging.error(f'请求 {URL} 失败: {e}')
    exit(1)

soup = BeautifulSoup(response.text, 'html.parser')

# 提取电信IP
telecom_ips = []
rows = soup.find_all('tr')
for row in rows:
    cells = row.find_all('td')
    if len(cells) >= 2:
        carrier = cells[0].get_text().strip()
        ip_cell = cells[1].get_text().strip()
        ip_match = re.search(IP_PATTERN, ip_cell)
        if ip_match and '电信' in carrier:
            telecom_ips.append(ip_match.group(0))
            if len(telecom_ips) >= MAX_IPS:
                break

# 如果网页没有足够电信IP，从所有 IP 里取前几个
if len(telecom_ips) < MAX_IPS:
    all_ips = re.findall(IP_PATTERN, response.text)
    unique_ips = [ip for ip in sorted(set(all_ips), key=lambda ip: [int(part) for part in ip.split('.')])
                  if ip not in telecom_ips]
    needed = MAX_IPS - len(telecom_ips)
    telecom_ips.extend(unique_ips[:needed])

# 添加端口和备注
result = []
for ip in telecom_ips:
    for port in TSL_PORTS:
        result.append(f"{ip}:{port}#官方优选")

# 写入文件
with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(result))

logging.info(f'已保存 {len(telecom_ips)} 个电信IP到 {OUTPUT_FILE} 文件。')
logging.info(f'电信IP列表: {telecom_ips}')
