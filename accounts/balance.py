from web3 import Web3

web3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/903b156a5f53406b97e4ddcde49cb3d9'))

balance = web3.eth.get_balance('0x908377865a0380d52fAdba305CB1d752d57C31F4')
print(balance)



private_key = '2471c1fcdf44a7b6a85068b43b89d0b54cff7555566c6ddb4e518cc2da18d08a'


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