from typing import Dict, Any, Optional
from web3 import Web3
from langchain_core.tools import tool

from src.utils.config import CELO_RPC_URL, CELO_CHAIN_ID

# Initialize Web3 connection to Celo
web3 = Web3(Web3.HTTPProvider(CELO_RPC_URL))


@tool
def get_latest_block_number() -> int:
    """
    Get the latest block number on the Celo blockchain.

    Returns:
        int: The latest block number
    """
    if not web3.is_connected():
        raise Exception("Failed to connect to Celo blockchain")

    return web3.eth.block_number


@tool
def get_block_info(block_number: Optional[int] = None) -> Dict[str, Any]:
    """
    Get information about a specific block on the Celo blockchain.

    Args:
        block_number: The block number to get information for.
                      If not provided, gets the latest block.

    Returns:
        Dict[str, Any]: Block information including timestamp, hash, etc.
    """
    if not web3.is_connected():
        raise Exception("Failed to connect to Celo blockchain")

    # If block_number is not provided, use the latest block
    if block_number is None:
        block_number = web3.eth.block_number

    # Get the block information
    block = web3.eth.get_block(block_number)

    # Convert block data to a serializable format
    return {
        "number": block.number,
        "hash": block.hash.hex(),
        "timestamp": block.timestamp,
        "transactions_count": len(block.transactions),
        "miner": block.miner,
        "gas_used": block.gasUsed,
        "gas_limit": block.gasLimit,
    }


@tool
def get_celo_stats() -> Dict[str, Any]:
    """
    Get basic statistics about the Celo blockchain.

    Returns:
        Dict[str, Any]: Statistics including chain ID, latest block, gas price, etc.
    """
    if not web3.is_connected():
        raise Exception("Failed to connect to Celo blockchain")

    return {
        "chain_id": CELO_CHAIN_ID,
        "latest_block": web3.eth.block_number,
        "gas_price": web3.eth.gas_price,
        "is_connected": web3.is_connected(),
        "peer_count": web3.net.peer_count if hasattr(web3.net, "peer_count") else None,
    }
