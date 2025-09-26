import requests
from bs4 import BeautifulSoup
import re

# 目标URL列表
urls = [
    'https://ip.164746.xyz/',  # 直接获取此网址上的 IP 和平均延迟
    'https://www.wetest.vip/page/cloudflare/address_v4.html',  # 获取云平台的往返延迟
]

# IP 匹配正则
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

telecom_ips = []

# 获取 https://ip.164746.xyz/ 的 IP 和延迟
try:
    response = requests.get(urls[0], timeout=8)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
except Exception as e:
    print(f'获取网址 {urls[0]} 失败: {e}')
    soup = None

if soup:
    rows = soup.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        if len(cells) < 2:  # 如果没有足够的列数据跳过
            continue
        ip_cell = cells[0].get_text(strip=True)
        latency_cell = cells[1].get_text(strip=True)  # 获取“平均延迟”列
        ip_matches = re.findall(ip_pattern, ip_cell)
        for ip in ip_matches:
            try:
                latency = float(latency_cell)  # 尝试将延迟转换为浮动值
            except ValueError:
                latency = None  # 如果无法转换延迟，设置为 None
            telecom_ips.append((ip, latency))  # 保存 IP 和延迟信息

# 获取 https://www.wetest.vip/page/cloudflare/address_v4.html 的电信IP和往返延迟
for url in urls[1:]:
    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
    except Exception as e:
        print(f'获取网页失败 {url}: {e}')
        continue

    if soup:
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 3:  # 必须有足够的列
                continue

            carrier = cells[0].get_text(strip=True)
            ip_cell = cells[1].get_text(strip=True)
            latency_text = cells[2].get_text(strip=True)  # 获取“往返延迟”列

            if '电信' in carrier:
                ip_matches = re.findall(ip_pattern, ip_cell)
                for ip in ip_matches:
                    try:
                        latency = float(latency_text)  # 获取往返延迟并转为浮动值
                    except ValueError:
                        latency = None  # 如果无法解析延迟，则设置为 None
                    telecom_ips.append((ip, latency))

# 按延迟从低到高排序
telecom_ips_sorted = sorted(telecom_ips, key=lambda x: (x[1] if x[1] is not None else float('inf')))

# 如果找到了IP才写入文件
if telecom_ips_sorted:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip, latency in telecom_ips_sorted:
            f.write(f"{ip}:443#官方优选\n")
    print(f'已保存 {len(telecom_ips_sorted)} 个IP到 ip.txt (按延迟排序)')
else:
    print('未找到IP，保留现有 ip.txt')
