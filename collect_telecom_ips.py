import requests

# 目标 URL
url = 'https://raw.githubusercontent.com/ZhiXuanWang/cf-speed-dns/refs/heads/main/ipTop10.html'

# 获取内容
response = requests.get(url)
content = response.text.strip()

# 按逗号分割 IP
ips = [ip.strip() for ip in content.split(',')]

# 写入文件并备注 CT
with open("addressesapi.txt", "w") as f:
    for ip in ips:
        f.write(f"{ip} #CT\n")

print(f"共拉取 {len(ips)} 个 IP，已写入 addressesapi.txt，并加上备注 #CT")
