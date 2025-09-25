import requests
from bs4 import BeautifulSoup
import re
import os

# 目标 URL
url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 匹配 IP 的正则
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 如果 ip.txt 存在则删除
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取表格行
    rows = soup.find_all('tr')
    telecom_ips = []

    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 2:
            carrier = cells[0].get_text().strip()
            ip_cell = cells[1].get_text().strip()
            ip_match = re.search(ip_pattern, ip_cell)
            if ip_match and '电信' in carrier:
                telecom_ips.append(ip_match.group(0))
        if len(telecom_ips) >= 5:
            break

    if not telecom_ips:
        raise ValueError("未找到电信 IP")

    # 排序和去重
    telecom_ips = sorted(set(telecom_ips), key=lambda ip: [int(x) for x in ip.split('.')])

    # 端口列表
    ports = ["443", "8443", "2053", "2083", "2087", "2096"]

    # 构建输出
    result = []
    for ip in telecom_ips:
        for port in ports:
            result.append(f"{ip}:{port} #狮城")

    # 写入文件
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for line in result:
            f.write(line + '\n')

    print(f"已保存 {len(result)} 条狮城 IP 到 ip.txt")
except Exception as e:
    print(f"抓取失败: {e}")
