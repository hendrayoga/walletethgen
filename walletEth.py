from web3 import Web3
from eth_account import Account
import logging
import requests

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to the Mode network RPC endpoint
web3 = Web3(Web3.HTTPProvider('https://mainnet.mode.network/'))

# Chain ID for the Mode network
chain_id = 0x868b

# Generate 10,000 wallets
num_wallets = 10000
wallets = []

for _ in range(num_wallets):
    acct = Account.create()
    wallets.append({
        'private_key': acct._private_key.hex(),
        'address': acct.address,
    })

logging.info('Wallet generation complete. Total wallets : %d', num_wallets)

with open('private_keys.txt', 'w') as f:
    for wallet in wallets:
        f.write(f"Address: {wallet['address']}, Private Key: {wallet['private_key']}\n")

logging.info('Private keys saved to private_keys.txt')

def test_rpc_connection(rpc_url):
    try:
        # Test connection by retrieving the provider URI
        provider_uri = rpc_url

        # Check if the provider URI matches the expected one
        if web3.provider.endpoint_uri == rpc_url:
            # If the URI matches, the connection is successful
            print(f"Successfully connected to {rpc_url}. Provider URI: {provider_uri}")
            return True
        else:
            # If the URI doesn't match, there might be an issue
            print(f"Connected to {rpc_url} but the provider URI doesn't match: {web3.provider.endpoint_uri}")
            return False

    except Exception as e:
        # Handle connection errors
        print(f"Failed to connect to {rpc_url}: {e}")
        return False

if __name__ == "__main__":
    rpc_url = input("Enter RPC URL to test: ")
    test_rpc_connection(rpc_url)

# Check the connection status by making a request to the node
def check_connection():
    try:
        # Call an RPC method to test the connection
        block_number = web3.eth.block_number
        return True
    except Exception as e:
        logging.error(f"Error checking connection: {str(e)}")
        return False

# Connect each wallet to the Mode network RPC endpoint and log connection status
for wallet in wallets:
    try:
        # Create an account object using the private key
        account = web3.eth.account.from_key(wallet['private_key'])

        # Check if the connection is successful
        if check_connection():
            logging.info(f"Wallet connected successfully to Mode network RPC endpoint. Address: {account.address}")
        else:
            logging.error(f"Failed to connect wallet to Mode network RPC endpoint. Address: {account.address}")

    except Exception as e:
        logging.error(f"Error connecting wallet to Mode network RPC endpoint. Address: {wallet['address']}, Error: {str(e)}")
