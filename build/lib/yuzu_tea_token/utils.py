from web3 import Web3

def validate_address(address: str) -> bool:
    """Validate Ethereum address"""
    return Web3.is_address(address)