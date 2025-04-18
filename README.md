# Yuzu Tea Token (YZTEA) - Python Package

A Python package to interact with the Yuzu Tea Token (YZTEA) ERC-20 token on the Tea Sepolia testnet (Chain ID: 10218).

## Features

- ✅ Send & receive YZTEA tokens
- ✅ Batch transfers (multi-send)
- ✅ Check token balances
- ✅ Auto-faucet for testnet TEA (gas tokens)
- ✅ Optimized for Tea Sepolia testnet

## Installation

```bash
pip install yuzu-tea-token
```

## Quick Start
### 1. Initialize the Contract
```python
from yuzu_tea import YuzuTeaToken

# Defaults to Tea Sepolia RPC
yuzu = YuzuTeaToken(
    contract_address="0xYourYZTEAContractAddress",
    private_key="your_private_key"  # Optional (needed for sending tokens)
)
```

### 2. Get Testnet TEA for Gas
Request testnet TEA for gas by using the faucet:
```python
yuzu.get_testnet_tea("0xYourWalletAddress")  # Request from faucet
```

### 3. Check Token Balance
Check the balance of YZTEA tokens:
```python
balance = yuzu.get_balance("0xUserAddress")
print(f"Balance: {balance} YZTEA")
```

### 4. Send YZTEA Tokens
Send YZTEA tokens to another address:
```python
tx_hash = yuzu.send_token(
    to_address="0xRecipientAddress",
    amount=100  # Amount in YZTEA
)
print(f"View on explorer: https://sepolia.tea.xyz/tx/{tx_hash}")
```

### 5. Batch Transfer
Send YZTEA tokens to multiple recipients:
```python
tx_hash = yuzu.batch_transfer(
    recipients=["0xAddr1", "0xAddr2"],
    amounts=[50, 100]  # 50 to Addr1, 100 to Addr2
)
```

## Examples
### Send Tokens to Multiple Users
```python
from yuzu_tea_token import YuzuTeaToken

yuzu = YuzuTeaToken(
    contract_address="0x123...abc",
    private_key="0xYourPrivateKey"
)

# Get testnet TEA
yuzu.get_testnet_tea("0xYourAddress")

# Batch transfer
tx_hash = yuzu.batch_transfer(
    recipients=["0xUser1", "0xUser2", "0xUser3"],
    amounts=[10, 20, 30]
)

print(f"Transaction: https://sepolia.tea.xyz/tx/{tx_hash}")
```

### Check Balance Before Sending
```python
balance = yuzu.get_balance("0xYourAddress")
if balance >= 50:
    yuzu.send_token("0xFriendAddress", 50)
else:
    print("Insufficient balance!")
```

## Network Information
- Network Name: Tea Sepolia
- RPC URL: https://tea-sepolia.g.alchemy.com/public
- Chain ID: 10218
- Block Explorer: https://sepolia.tea.xyz
- Faucet: https://faucet-sepolia.tea.xyz

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.