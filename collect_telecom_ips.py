import requests
from bs4 import BeautifulSoup
import os

url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 删除旧文件
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # 网页里电信 IP 通常在 <td> 或 <li> 标签里包含“电信”
    ips = []
    for tag in soup.find_all(text=True):
        text = tag.strip()
        if '电信' in text:
            # 提取 IP
            ip = text.split()[0]  # 假设 IP 在备注前
            ips.append(ip)
        if len(ips) >= 5:
            break

    # 写入 ip.txt，添加备注“狮城”
    with open('ip.txt', 'w') as f:
        for ip in ips:
            f.write(f"{ip} # 狮城\n")

    print(f"已保存 {len(ips)} 个电信 IP 到 ip.txt")
except Exception as e:
    print(f"拉取 IP 失败: {e}")
