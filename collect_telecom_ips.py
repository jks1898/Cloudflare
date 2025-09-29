import requests
import re
import os

# 目标URL
url = 'https://ip.164746.xyz/'

# 匹配 IPv4 地址的正则
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# 获取 IP 列表
response = requests.get(url)
ips = re.findall(ip_pattern, response.text)

# 去重并测试 IP 可用性
def ping_ip(ip):
    param = "-n" if os.name == "nt" else "-c"
    response = os.system(f"ping {param} 1 {ip} >nul 2>&1")
    return response == 0

valid_ips = []
for ip in set(ips):  # 去重
    if ping_ip(ip):
        valid_ips.append(ip)
    if len(valid_ips) >= 5:  # 找到 5 个可用 IP 就停止
        break

# 写入文件
with open("addressesapi.txt", "w") as f:
    for ip in valid_ips:
        f.write(f"{ip} #CT\n")

print(f"共抓取 {len(ips)} 个 IP，写入 {len(valid_ips)} 个可用 IP")
