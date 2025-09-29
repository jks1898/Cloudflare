import requests
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 目标 URL
url = 'https://www.wetest.vip/page/cloudflare/total_v4.html'

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

try:
    # 请求网页内容
    response = session.get(url, headers=headers, timeout=5)
    response.raise_for_status()
    html_content = response.text

    # 提取所有合法 IP（允许重复）
    ips = re.findall(ip_pattern, html_content)

    # 覆盖写入 addressesapi.txt
    with open('addressesapi.txt', 'w', encoding='utf-8') as f:
        for ip in ips:
            f.write(f"{ip} #CT\n")

    print(f"共抓取 {len(ips)} 个 IP（含重复），已写入 addressesapi.txt 文件。")

except requests.exceptions.RequestException as e:
    print(f"请求 {url} 失败: {e}")
