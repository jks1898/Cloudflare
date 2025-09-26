import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re

# 目标URL列表
urls = [
    'https://ip.164746.xyz/',  # 直接获取此网址上的 IP
    'https://www.wetest.vip/page/cloudflare/address_v4.html',  # 获取云平台的电信IP
]

# IP 匹配正则
ip_pattern = r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
             r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'

telecom_ips = []

# 异步获取网页内容
async def fetch(url, session):
    try:
        async with session.get(url, timeout=8) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        print(f'获取网址 {url} 失败: {e}')
        return None

# 异步解析 https://ip.164746.xyz/ 的 IP
async def parse_164746_xyz(session):
    url = urls[0]
    html = await fetch(url, session)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 1:  # 如果没有足够的列数据跳过
                continue
            ip_cell = cells[0].get_text(strip=True)
            ip_matches = re.findall(ip_pattern, ip_cell)
            for ip in ip_matches:
                telecom_ips.append(ip)  # 只保存 IP

# 异步解析 https://www.wetest.vip/page/cloudflare/address_v4.html 的电信IP
async def parse_wetest_vip(session):
    url = urls[1]
    html = await fetch(url, session)
    if html:
        soup = BeautifulSoup(html, 'html.parser')
        rows = soup.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) < 2:  # 必须有足够的列
                continue
            carrier = cells[0].get_text(strip=True)
            ip_cell = cells[1].get_text(strip=True)

            if '电信' in carrier:
                ip_matches = re.findall(ip_pattern, ip_cell)
                for ip in ip_matches:
                    telecom_ips.append(ip)

# 主函数：并发请求并解析
async def main():
    async with aiohttp.ClientSession() as session:
        # 异步并发抓取和解析两个网页
        await asyncio.gather(parse_164746_xyz(session), parse_wetest_vip(session))

    # 写入文件
    if telecom_ips:
        with open('ip.txt', 'w', encoding='utf-8') as f:
            for ip in telecom_ips:
                f.write(f"{ip}:443#官方优选\n")
        print(f'已保存 {len(telecom_ips)} 个IP到 ip.txt')
    else:
        print('未找到IP，保留现有 ip.txt')

# 运行异步事件循环
if __name__ == "__main__":
    asyncio.run(main())
