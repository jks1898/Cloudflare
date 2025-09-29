import requests
import re

# 目标URL
url = 'https://ip.164746.xyz/ipTop10.html'

# 获取 HTML 内容
response = requests.get(url)
html_content = response.text

# 匹配 IPv4 地址的正则
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

# 提取所有 IP 地址
ips = re.findall(ip_pattern, html_content)

# 因为页面只有 10 个 IP，所以直接取前 10 个
top_ips = ips[:10]

# 写入文件并备注 CT
with open("addressesapi.txt", "w") as f:
    for ip in top_ips:
        f.write(f"{ip} #CT\n")

print(f"共抓取 {len(ips)} 个 IP，写入 {len(top_ips)} 个 IP，已加上备注 #CT")
