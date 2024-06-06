import requests
from bs4 import BeautifulSoup
import json
import re
import sys
import os

# URL of the GeckoTerminal pools page
url = "https://www.geckoterminal.com/solana/pools/32D4zRxNc1EssbJieVHfPhZM3rH6CzfUPrWUuWxD9prG"

# Token variables
token1 = "USDC"
token2 = "USDT"


# Send a GET request to the URL
print('Loading data from https://www.geckoterminal.com/solana/pools/32D4zRxNc1EssbJieVHfPhZM3rH6CzfUPrWUuWxD9prG ...')
response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    with open('pool_data.html', 'w') as f:
        f.write(str(soup))
    
    with open('pool_data.html', 'r') as file_:
        lines = file_.readlines()
    
    # Iterate through each line to find the target value
    for line in lines:
        if 'pooled USDC' in line:
            # Use regular expressions to find the values after 'pooled USDC' and 'pooled USDT'
            usdc_match = re.search(rf'pooled {token1} is ([\d,\.]+)', line)
            usdt_match = re.search(rf'pooled {token2} is ([\d,\.]+)', line)
            
            if usdc_match and usdt_match:
                usdc_value = float(usdc_match.group(1).replace(',', ''))
                usdt_value = float(usdt_match.group(1).replace(',', ''))
            
                print(f"Extracted USDC value: {usdc_value}")
                print(f"Extracted USDT value: {usdt_value}")
            else:
                print("Values not found in the line")

    os.remove('pool_data.html')



