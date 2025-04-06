#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# send_token_example.py
# Example script for sending YZTEA tokens to a single address
# License: GNU GPL v3

from yuzu_tea_token import YuzuTeaToken  # Changed import
from web3 import Web3

# Configuration
CONTRACT_ADDRESS = "0x71171Bca935b1271fd3470d2702989514995DAb2"  # YZTEA contract address
PRIVATE_KEY = "your_private_key_here"            # Never commit this to version control!
RECIPIENT_ADDRESS = "0xRecipientAddressHere"     # Address to receive tokens
AMOUNT_TO_SEND = 50                              # Amount of YZTEA tokens to send

def main():
    # Initialize Yuzu Tea Token instance
    print("Initializing Yuzu Tea Token connection...")
    yuzu = YuzuTeaToken(
        contract_address=CONTRACT_ADDRESS,
        private_key=PRIVATE_KEY
    )

    # Verify connection
    if not yuzu.web3.is_connected():
        print("❌ Failed to connect to Tea Sepolia network")
        return

    print("✅ Connected to Tea Sepolia network")

    # Get sender address from private key
    sender_address = Web3().eth.account.from_key(PRIVATE_KEY).address
    print(f"Sender address: {sender_address}")

    # Check sender balance before sending
    print("\nChecking balances...")
    try:
        sender_balance = yuzu.get_balance(sender_address)
        recipient_balance = yuzu.get_balance(RECIPIENT_ADDRESS)

        print(f"Current balance:")
        print(f"- Sender: {sender_balance} YZTEA")
        print(f"- Recipient: {recipient_balance} YZTEA")

        if sender_balance < AMOUNT_TO_SEND:
            print(f"\n❌ Insufficient balance. Need {AMOUNT_TO_SEND} YZTEA but only have {sender_balance}")
            return

    except Exception as e:
        print(f"❌ Error checking balances: {e}")
        return

    # Send tokens
    print(f"\nSending {AMOUNT_TO_SEND} YZTEA to {RECIPIENT_ADDRESS}...")
    try:
        tx_hash = yuzu.send_token(
            to_address=RECIPIENT_ADDRESS,
            amount=AMOUNT_TO_SEND
        )
        
        print(f"✅ Transaction successful!")
        print(f"Transaction hash: {tx_hash}")
        print(f"View on explorer: https://sepolia.tea.xyz/tx/{tx_hash}")

    except Exception as e:
        print(f"❌ Error sending tokens: {e}")

if __name__ == "__main__":
    print("YZTEA Token Transfer Example")
    print("---------------------------")
    main()