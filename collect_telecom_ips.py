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
        if len(cells) < 3:
            continue

        carrier = cells[0].get_text(strip=True)
        ip_cell = cells[1].get_text(strip=True)
        latency_text = cells[2].get_text(strip=True)  # 网页里的“往返延迟”列

        if '电信' in carrier:
            # 提取所有 IP 地址
            ip_matches = re.findall(ip_pattern, ip_cell)
            if ip_matches:
                # 处理延迟文本去除 ms 单位
                try:
                    latency = float(latency_text.replace("ms", "").strip())
                except ValueError:
                    latency = float('inf')  # 无法解析放到最后
                for ip in ip_matches:
                    telecom_ips.append((ip, latency))

# 按网页“往返延迟”列从小到大排序
telecom_ips_sorted = sorted(
    [item for item in telecom_ips if item[1] != float('inf')],
    key=lambda x: x[1]
)

# 判断是否有有效的电信 IP 并写入文件
if telecom_ips_sorted:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip, _ in telecom_ips_sorted[:10]:  # 可限制保存数量
            f.write(f"{ip}:443#官方优选\n")
    print(f'已保存 {len(telecom_ips_sorted)} 个电信IP到 ip.txt (按网页往返延迟排序)')
else:
    print('未找到有效的电信IP，保留现有的 ip.txt')
