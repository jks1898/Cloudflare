name: Update Telecom IPs

on:
  schedule:
    # 每两小时的整点，UTC = 北京时间 -8小时
    - cron: '0 */2 * * *'
  workflow_dispatch: # 手动触发

permissions:
  contents: write

jobs:
  update-ip-list:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests beautifulsoup4

      - name: Run collect_telecom_ips.py
        run: python collect_telecom_ips.py

      - name: Commit and push ip.txt
        run: |
          git config --local user.name "github-actions"
          git config --local user.email "actions@github.com"
          git add ip.txt
          git commit -m "Update telecom IPs" || echo "No changes to commit"
          git push
