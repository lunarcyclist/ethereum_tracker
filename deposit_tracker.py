import requests
import json
import time
import csv
import os

# Function to save a deposit into a CSV file
def save_deposit(block_number, block_timestamp, fee, tx_hash, pubkey):
    # Define the file name
    file_name = 'deposits.csv'

    # Check if the file exists
    file_exists = os.path.isfile(file_name)

    # Open the file in append mode
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)

        # If the file doesn't exist, write the header
        if not file_exists:
            writer.writerow(['blockNumber', 'blockTimestamp', 'fee', 'hash', 'pubkey'])

        # Log the data being saved
        print(f"Saving deposit: blockNumber={block_number}, blockTimestamp={block_timestamp}, fee={fee}, hash={tx_hash}, pubkey={pubkey}")
        
        # Write the deposit data to the CSV file
        writer.writerow([block_number, block_timestamp, fee, tx_hash, pubkey])

    print(f"Data saved for transaction {tx_hash}.")

# Alchemy API URL
ALCHEMY_API_URL = 'https://eth-mainnet.g.alchemy.com/v2/NLvZ_9hZFNv4aGHYRZmadwT4eDmpySH3'

# Beacon Deposit Contract address
BEACON_DEPOSIT_CONTRACT = '0x00000000219ab540356cBB839Cbe05303d7705Fa'

# Function to fetch the latest block number
def get_latest_block_number():
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_blockNumber",
        "params": []
    }

    response = requests.post(ALCHEMY_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        block_number_hex = response.json()['result']
        return int(block_number_hex, 16)
    else:
        print(f"Error fetching latest block: {response.status_code}")
        return None

# Function to fetch block details by number
def get_block_by_number(block_number):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }

    data = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "eth_getBlockByNumber",
        "params": [hex(block_number), True]
    }

    response = requests.post(ALCHEMY_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching block: {response.status_code}")
        return None

# Function to parse logs for contract-based deposits
def parse_logs(logs):
    for log in logs:
        address = log.get('address')
        topics = log.get('topics', [])
        data = log.get('data')

        print(f"Log Address: {address}")
        print(f"Topics: {topics}")
        print(f"Data: {data}")

        if topics and topics[0] == "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef":  # Example signature
            deposit_value = int(data, 16) / (10**18)
            return deposit_value
    return 0

# Function to handle regular deposit transactions
def handle_regular_deposit(tx_data):
    tx_result = tx_data.get('result', {})
    value_wei = tx_result.get('value')

    if value_wei is None or value_wei == '0x':
        print(f"No value found in transaction or invalid format. Skipping regular deposit handling.")
        return 0

    value_eth = int(value_wei, 16) / (10**18)
    return value_eth

# Function to parse and analyze transaction details
def parse_transaction(tx):
    from_address = tx.get('from')
    to_address = tx.get('to')
    tx_hash = tx.get('hash')
    gas_price = int(tx.get('gasPrice'), 16)
    gas_used = int(tx.get('gas'), 16)
    block_number = int(tx.get('blockNumber'), 16)
    logs = tx.get('logs', [])

    pubkey = from_address  # Assuming the `pubkey` is the 'from' address (modify if incorrect)

    fee = (gas_price * gas_used) / (10**18)

    block_data = get_block_by_number(block_number)
    if block_data:
        block_timestamp = int(block_data['result']['timestamp'], 16)
        block_timestamp_human = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(block_timestamp))
    else:
        block_timestamp_human = 'N/A'

    deposit_value = parse_logs(logs)

    if deposit_value == 0:
        deposit_value = handle_regular_deposit(tx)

    print(f"From: {from_address}")
    print(f"To: {to_address}")
    print(f"Transaction fee (ETH): {fee}")
    print(f"Block Number: {block_number}")
    print(f"Block Timestamp: {block_timestamp_human}")
    print(f"Deposit Value (ETH): {deposit_value}")

    if to_address and to_address.lower() == BEACON_DEPOSIT_CONTRACT.lower() and deposit_value > 0:
        if logs:  # If logs are present, it's a contract-based deposit
            print("This is a contract-based deposit.")
        else:  # If no logs, it's a regular transaction-based deposit
            print("This is a regular deposit transaction.")
        # Save to the CSV file
        save_deposit(block_number, block_timestamp_human, fee, tx_hash, pubkey)
    else:
        print("No deposit found.")

# Main function to track deposits
def track_deposits():
    last_checked_block = get_latest_block_number()
    print(f"Starting tracking from block: {last_checked_block}")

    while True:
        try:
            latest_block = get_latest_block_number()
            if latest_block and latest_block > last_checked_block:
                print(f"New block detected: {latest_block}. Checking for deposits...")

                for block_num in range(last_checked_block + 1, latest_block + 1):
                    block_data = get_block_by_number(block_num)
                    if block_data and 'result' in block_data:
                        transactions = block_data['result']['transactions']
                        for tx in transactions:
                            parse_transaction(tx)

                last_checked_block = latest_block
            else:
                print("No new blocks, waiting...")

            time.sleep(10)

        except KeyboardInterrupt:
            print("\nProcess interrupted by user. Exiting...")
            break

# Main script
if __name__ == "__main__":
    track_deposits()

