import requests
from bs4 import BeautifulSoup
import re
import os

url = 'https://www.wetest.vip/page/cloudflare/address_v4.html'

# 匹配 IPv4
ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'

# 删除旧文件
if os.path.exists('ip.txt'):
    os.remove('ip.txt')

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    html_content = response.text

    # 使用正则找到所有 IP
    ip_matches = re.findall(ip_pattern, html_content)

    # 筛选电信 IP（简单规则：第一位为 1-59 属电信网段，也可以结合 GeoIP 做精确判断）
    telecom_ips = [ip for ip in ip_matches if ip.startswith(('1','27','36','39','58'))]

    # 取前五个，并加备注“狮城”
    top5 = telecom_ips[:5]
    with open('ip.txt', 'w') as f:
        for ip in top5:
            f.write(f"{ip} # 狮城\n")
    print(f"已保存 {len(top5)} 个电信 IP 到 ip.txt")
except Exception as e:
    print(f"拉取 IP 失败: {e}")
