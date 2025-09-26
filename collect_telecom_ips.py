import requests
from bs4 import BeautifulSoup
import re
import heapq

# 目标URL
url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 匹配IP的正则（准确匹配有效的IP地址）
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# 存储 (IP, 往返延迟)
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
        latency_text = cells[2].get_text(strip=True)  # 假设第三列是延迟数据

        # 匹配IP地址并筛选电信的IP
        ip_match = re.search(ip_pattern, ip_cell)
        if ip_match and '电信' in carrier:
            ip = ip_match.group(0)

            # 解析往返延迟（去除非数字字符）
            try:
                latency = float(re.sub(r'[^0-9.]', '', latency_text))
            except ValueError:
                latency = float('inf')  # 无法解析时默认为最大延迟

            telecom_ips.append((ip, latency))

# 排序并获取前 5 个延迟最小的电信IP（虽然只剩下5个，所以这里只是一个排序操作）
telecom_ips_sorted = sorted(telecom_ips, key=lambda x: x[1])

# 只有找到电信 IP 才写入，否则保留旧文件
if telecom_ips_sorted:
    with open('ip.txt', 'w', encoding='utf-8') as f:
        for ip, latency in telecom_ips_sorted:
            f.write(f"{ip}:443#官方优选\n")
    print(f'已保存 {len(telecom_ips_sorted)} 个电信IP到 ip.txt (按往返延迟排序)')
else:
    print('未找到有效的电信IP，保留现有的 ip.txt')
