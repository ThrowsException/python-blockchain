import hashlib
import json
import logging

from time import time
from uuid import uuid4

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)


class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain
        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
                'index': len(self.chain) + 1,
                'timestamp': time(),
                'transactions': self.current_transactions,
                'proof': proof,
                'previous_hash': previous_hash or self.hash(self.chain[-1]),
                }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Add a new transaction to the transactions list

        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> The index of the Block that will hold the
            transaction
        """

        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    def proof_of_work(self, last_proof):
        """
        Simple Proof of Work Algorithm:
        - find a number p such that hash (pp`) contains leading 4 zeroes,
            where p is the previous p`

        - p is the previous proof, p` is the new proof


        :param last_proof: <int>
        :return: <int>
        """

        logger.debug('Do proof of work')
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            logger.debug(proof)
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validates the proof: Does hash(last_proof, proof) contain 4 leading zeroes?

        :param last_proof: <int> Previous Proof
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False otherwise
        """

        guess = '{}{}'.format(last_proof, proof).encode()
        logger.info(guess)
        guess_hash = hashlib.sha256(guess).hexdigest()
        logger.info(guess_hash)
        return guess_hash[:4] == "0000"

    @staticmethod
    def hash(block):
        """
        Create a SHA-256 hash of a Block

        :param block: <dict> Block
        :return: <str>
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        Returns last Block in the chain
        """

        return self.chain[-1]
