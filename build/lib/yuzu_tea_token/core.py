from web3 import Web3
from web3.middleware import geth_poa_middleware
from typing import List, Union
from .exceptions import YuzuTeaError

class YuzuTeaToken:
    def __init__(
        self,
        rpc_url: str = "https://tea-sepolia.g.alchemy.com/public",
        contract_address: str = None,
        private_key: str = None,
        chain_id: int = 10218  # Tea Sepolia Chain ID
    ):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        
        # Support for PoA chains (if needed)
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        self.contract_address = contract_address
        self.private_key = private_key
        self.chain_id = chain_id
        
        # ABI for ERC-20 + YuzuTea custom functions
        self.abi = [
            # Standard ERC-20 ABI
            {"constant":True,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},
            {"constant":True,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":False,"stateMutability":"view","type":"function"},
            {"constant":True,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":False,"stateMutability":"view","type":"function"},
            {"constant":True,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":False,"stateMutability":"view","type":"function"},
            {"constant":False,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"},
            
            # YuzuTea Custom Functions
            {"constant":False,"inputs":[{"name":"recipients","type":"address[]"},{"name":"amounts","type":"uint256[]"}],"name":"batchTransfer","outputs":[],"payable":False,"stateMutability":"nonpayable","type":"function"}
        ]
        
        if contract_address:
            self.contract = self.web3.eth.contract(
                address=self.web3.to_checksum_address(contract_address),
                abi=self.abi
            )
    
    def send_token(
        self,
        to_address: str,
        amount: Union[int, float],
        gas_price: int = None
    ) -> str:
        """Send YZTEA tokens to a single address on Tea Sepolia"""
        if not self.private_key:
            raise YuzuTeaError("Private key is required for sending tokens")
        
        account = self.web3.eth.account.from_key(self.private_key)
        to_address = self.web3.to_checksum_address(to_address)
        
        # Convert amount to wei
        amount_wei = self.web3.to_wei(amount, 'ether')
        
        # Build transaction
        tx = self.contract.functions.transfer(
            to_address,
            amount_wei
        ).build_transaction({
            'chainId': self.chain_id,  # Tea Sepolia Chain ID
            'gas': 200000,
            'gasPrice': gas_price or self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(account.address),
        })
        
        # Sign and send
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return tx_hash.hex()
    
    def batch_transfer(
        self,
        recipients: List[str],
        amounts: List[Union[int, float]],
        gas_price: int = None
    ) -> str:
        """Batch transfer YZTEA tokens on Tea Sepolia"""
        if len(recipients) != len(amounts):
            raise YuzuTeaError("Recipients and amounts must have the same length")
        
        if not self.private_key:
            raise YuzuTeaError("Private key is required for batch transfer")
        
        account = self.web3.eth.account.from_key(self.private_key)
        
        # Convert addresses to checksum format
        recipients = [self.web3.to_checksum_address(addr) for addr in recipients]
        
        # Convert amounts to wei
        amounts_wei = [self.web3.to_wei(amt, 'ether') for amt in amounts]
        
        # Build transaction
        tx = self.contract.functions.batchTransfer(
            recipients,
            amounts_wei
        ).build_transaction({
            'chainId': self.chain_id,  # Tea Sepolia Chain ID
            'gas': 200000 * len(recipients),  # Adjust gas based on batch size
            'gasPrice': gas_price or self.web3.eth.gas_price,
            'nonce': self.web3.eth.get_transaction_count(account.address),
        })
        
        # Sign and send
        signed_tx = self.web3.eth.account.sign_transaction(tx, self.private_key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        return tx_hash.hex()
    
    def get_balance(self, address: str) -> float:
        """Get YZTEA token balance in human-readable format"""
        address = self.web3.to_checksum_address(address)
        balance_wei = self.contract.functions.balanceOf(address).call()
        return self.web3.from_wei(balance_wei, 'ether')
    
    def get_testnet_tea(self, address: str) -> bool:
        """Request testnet TEA tokens from faucet (for gas fees)"""
        import requests
        
        response = requests.post(
            "https://faucet-sepolia.tea.xyz/",
            json={"address": address}
        )
        return response.status_code == 200