import requests
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 目标 URL 列表
urls = [
    'https://ip.164746.xyz/',
    'https://www.wetest.vip/page/cloudflare/total_v4.html'
]

# 匹配 IPv4 地址的正则（严格写法）
ip_pattern = (
    r'\b(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\b'
)

# Session + 重试
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

# 伪装 UA
headers = {"User-Agent": "Mozilla/5.0 (compatible; IPCollector/1.0)"}

all_ips = []

try:
    for url in urls:
        response = session.get(url, headers=headers, timeout=5)
        response.raise_for_status()
        html_content = response.text

        # 提取所有合法 IP
        ips = re.findall(ip_pattern, html_content)
        all_ips.extend(ips)

        print(f"从 {url} 抓取到 {len(ips)} 个 IP")

    # 去重但保留顺序
    unique_ips = list(dict.fromkeys(all_ips))

    # 覆盖写入 addressesapi.txt
    with open('addressesapi.txt', 'w', encoding='utf-8') as f:
        for ip in unique_ips:
            f.write(f"{ip} #CT\n")

    print(f"总共写入 {len(unique_ips)} 个唯一 IP 到 addressesapi.txt 文件。")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
