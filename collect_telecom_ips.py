import requests
from bs4 import BeautifulSoup
import re

# 只从这个地址获取
url = 'https://ip.164746.xyz/'

# 匹配 IPv4 地址
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

all_ips = set()

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    ips = re.findall(ip_pattern, text)
    all_ips.update(ips)
except Exception as e:
    print(f"Error fetching {url}: {e}")

# 只写入前五个 IP
with open("addressesapi.txt", "w") as f:
    for ip in sorted(all_ips)[:5]:
        f.write(f"{ip} #CT\n")
