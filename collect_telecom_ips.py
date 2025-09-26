import requests
from bs4 import BeautifulSoup
import re
import os
import heapq

# 目标URL
url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 匹配IP的正则（准确匹配有效的IP地址）
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# 存储 (IP, 峰值速度)
telecom_ips = []

try:
    # 获取网页内容
    response = requests.get(url, timeout=8)
    response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
    soup = BeautifulSoup(response.text, 'html.parser')

except requests.exceptions.RequestException as e:
    print(f'网络请求失败: {e}')
    soup = None  # 如果请求失败，后续解析跳过

except Exception as e:
    print(f'解析网页时发生错误: {e}')
    soup = None  # 如果解析失败，后续跳过

# 网页解析
if soup:
    rows = soup.find_all('tr')
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 3:
            continue  # 如果不包含所需数据，跳过该行

        carrier = cells[0].get_text(strip=True)
        ip_cell = cells[1].get_text(strip=True)
        speed_text = cells[2].get_text(strip=True)

        # 匹配IP地址并筛选电信的IP
        ip_match = re.search(ip_pattern, ip_cell)
        if ip_match and '电信' in carrier:
            ip = ip_match.group(0)

            # 解析峰值速度
            try:
                speed = float(re.sub(r'[^0-9.]', '', speed_text))
            except ValueError:
                speed = 0.0  # 如果无法解析速度，则默认0

            telecom_ips.append((ip, speed))

# 获取前 5 个速度最快的电信IP
top_telecom_ips = heapq.nlargest(5, telecom_ips, key=lambda x: x[1])

# 只有找到电信 IP 才写入，否则保留旧文件
if top_telecom_ips:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip, speed in top_telecom_ips:
            f.write(f"{ip}:443#官方优选\n")
    print(f'已保存 {len(top_telecom_ips)} 个电信IP到 ip.txt (按峰值速度排序)')
else:
    print('未找到有效的电信IP，保留现有的 ip.txt')
