name: Update IP List

on:
  schedule:
    # UTC 0:00 和 12:00 对应香港 08:00 和 20:00
    - cron: '0 0,12 * * *'
    # 每小时一次自检，确保漏掉的触发可以补上
    - cron: '0 * * * *'
  workflow_dispatch:

permissions:
  contents: write
  actions: write

jobs:
  update-ip-list:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests beautifulsoup4
        
    - name: Run script with retry
      run: |
        for i in 1 2 3; do
          python collect_telecom_ips.py && break || echo "Attempt $i failed, retrying..."
          sleep 10
        done
        
    - name: Commit and push changes if any
      run: |
        git config --local user.email "actions@github.com"
        git config --local user.name "GitHub Action"
        if [ -n "$(git status --porcelain)" ]; then
          git add .
          git commit -m "Automatic update"
          git push
        else
          echo "No changes detected, skipping commit."
