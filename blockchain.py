class BlockChain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

    def new_block(self):
        """
        Create a new Block to add to the chain
        """
        pass

    def new transaction(self):
        """
        Add a new transaction to the transactions list
        """
        pass

    @staticmethod
    def hash(block):
        """
        Hashes a block
        """
        pass

    @property
    def last_block(self):
        """
        Returns if last Block in the chain
        """
        pass
