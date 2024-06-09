from web3 import Web3

infura_url = 'https://sepolia.infura.io/v3/903b156a5f53406b97e4ddcde49cb3d9'
web3 = Web3(Web3.HTTPProvider(infura_url))

if web3.is_connected():
    print("Connected to Sepolia network")
else:
    print("Failed to connect to Sepolia network")

# Replace with your token contract address and ABI
token_address = '0x51A23017B3e788C7E7E373E2b759178ED91137Dd'
token_abi = [
    {"inputs": [], "stateMutability": "nonpayable", "type": "constructor"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "owner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "spender", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Approval", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint8", "name": "version", "type": "uint8"}], "name": "Initialized", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "from", "type": "address"}, {"indexed": True, "internalType": "address", "name": "to", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event"},
    {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}, {"internalType": "address", "name": "spender", "type": "address"}], "name": "allowance", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "approve", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "balanceOf", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "burn", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "account", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "burnFrom", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "decimals", "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "subtractedValue", "type": "uint256"}], "name": "decreaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "spender", "type": "address"}, {"internalType": "uint256", "name": "addedValue", "type": "uint256"}], "name": "increaseAllowance", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "_owner", "type": "address"}, {"internalType": "string", "name": "_name", "type": "string"}, {"internalType": "string", "name": "_symbol", "type": "string"}, {"internalType": "uint8", "name": "_decimals", "type": "uint8"}, {"internalType": "uint256", "name": "_initialSupply", "type": "uint256"}], "name": "initialize", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "maxSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "name", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "symbol", "outputs": [{"internalType": "string", "name": "", "type": "string"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "totalSupply", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transfer", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "from", "type": "address"}, {"internalType": "address", "name": "to", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "transferFrom", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "nonpayable", "type": "function"}
]
# Create contract instance
contract = web3.eth.contract(address=token_address, abi=token_abi)

def get_balance(address):
    balance = contract.functions.balanceOf(address).call()
    decimals = contract.functions.decimals().call()
    return balance/ (10 ** decimals) # Use the correct unit conversion if needed

# Replace with the address you want to check
address = '0x908377865a0380d52fAdba305CB1d752d57C31F4'

balance = get_balance(address)
print(f'Balance of address {address}: {balance} tokens')



#from_account = '0x908377865a0380d52fAdba305CB1d752d57C31F4'
#to_account = ''

#address1 = Web3.toChecksumAddress(from_account)
#address2 = Web3.toChecksumAddress(to_account)

#nonce = web3.eth.getTransactionCount(address1)

#tx = {
#   'nonce' : nonce,
#    'to' : address2,
 #   'value' : web3.toWei(0.001, 'ether'),
  #  'gas' : 21000,
   # 'gasPrice' : web3.toWei(40, 'gwei')
#}

#signed_tx = web3.eth.account.signTransaction(tx, private_key)

#tx_transaction = web3.eth.sendRawTransaction(signed_tx.rawTransaction)