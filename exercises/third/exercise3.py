import json
import os
import re
import requests
from bs4 import BeautifulSoup
import numpy as np

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
    
    # Save the parsed HTML to a file
    with open('pool_data.html', 'w') as f:
        f.write(str(soup))

    # Read the file and process the content
    with open('pool_data.html', 'r') as file_:
        lines = file_.readlines()

    # Initialize values for token1 and token2
    token1_value = None
    token2_value = None

    # Iterate through each line to find the target value
    for line in lines:
        if f'pooled {token1}' in line:
            # Use regular expressions to find the values after 'pooled <token1>' and 'pooled <token2>'
            token1_match = re.search(rf'pooled {token1} is ([\d,\.]+)', line)
            token2_match = re.search(rf'pooled {token2} is ([\d,\.]+)', line)

            if token1_match and token2_match:
                #token1_value = float(token1_match.group(1).replace(',', ''))
                #token2_value = float(token2_match.group(1).replace(',', ''))
                token1_value = np.float64(token1_match.group(1).replace(',', ''))
                token2_value = np.float64(token2_match.group(1).replace(',', ''))

                print(f"Extracted {token1} value: {token1_value}")
                print(f"Extracted {token2} value: {token2_value}")
            else:
                print("Values not found in the line")

    # Delete the file after processing
    os.remove('pool_data.html')
    print("File 'pool_data.html' has been deleted.")

# Load the existing JSON data
json_file = 'data.json'
with open(json_file, 'r') as file:
    data = json.load(file)

# Add the new section to the 'venues' key
if token1_value is not None and token2_value is not None:
    data['venues']['METEORA_USDC_USDT'] = {
        'reserves': {
            token1: f"{token1_value:.18f}".replace('.','_'),
            token2: f"{token2_value:.18f}".replace('.','_')
        }
    }

    # Save the updated JSON back to the file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)
    print("New venue added to the JSON file.")
else:
    print("No valid token values were extracted.")

