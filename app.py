import uuid

import tornado.ioloop
import tornado.web
import tornado.escape

from blockchain import BlockChain

blockchain = BlockChain()
node_identifier = str(uuid.uuid4()).replace('-', '')

class MineHandler(tornado.web.RequestHandler):
    def get(self):

        last_block = blockchain.last_block
        last_proof = last_block['proof']
        proof = blockchain.proof_of_work(last_proof)

        blockchain.new_transaction(
                sender="0",
                recipient=node_identifier,
                amount=1,
            )

        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)

        response = {
                'message': "New Block Forged",
                'index': block['index'],
                'transactions': block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
            }

        self.write(response)

class TransactionHandler(tornado.web.RequestHandler):
    def post(self):
        values = tornado.escape.json_decode(self.request.body)

        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            tornado.web.send_error()

        index = blockchain.new_transaction(
                values['sender'],
                values['recipient'],
                values['amount']
            )
        self.write(tonado.escape.json_encode(
            {'message': 'Transaction will be added to the Block {}'.format(index)}
        ))


class ChainHandler(tornado.web.RequestHandler):
    def get(self):

        self.write(tornado.escape.json_encode(blockchain.chain))

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/transaction", TransactionHandler),
        (r"/mine", MineHandler),
        (r"/chain", ChainHandler),
    ])

    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()
