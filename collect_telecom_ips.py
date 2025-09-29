import requests
import re
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# 目标 URL
url = 'https://ip.164746.xyz/'

# 匹配 IPv4 的正则（支持被 HTML 标签或空格包围）
ip_pattern = re.compile(
    r'(?<!\d)(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)\.'
    r'(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]?\d)(?!\d)'
)

# Session + 重试
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500,502,503,504])
session.mount("http://", HTTPAdapter(max_retries=retries))
session.mount("https://", HTTPAdapter(max_retries=retries))

headers = {"User-Agent": "Mozilla/5.0 (compatible; IPCollector/1.0)"}

try:
    response = session.get(url, headers=headers, timeout=8)
    response.raise_for_status()
    html_content = response.text

    # 提取所有 IP，不去重
    ips = ip_pattern.findall(html_content)

    # 写入 addressesapi.txt
    with open('addressesapi.txt', 'w', encoding='utf-8') as f:
        for ip in ips:
            f.write(f"{ip} #CT\n")

    print(f"总共抓取并写入 {len(ips)} 个 IP 到 addressesapi.txt 文件。")

except requests.exceptions.RequestException as e:
    print(f"请求失败: {e}")
