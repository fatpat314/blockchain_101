import hashlib
from time import time
import json


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def proof_of_work(self, last_proof):
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    # creates new block and adds them to an exsisting chain
    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            # 'trasaction_list':
            'proof': proof,
            previous_hash: previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    # adds a new transaction to already exsisting transactions
    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.current_transactions.append(transaction)
        return self.last_block['index'] + 1


    @staticmethod
    #used for hashing a block
    def hash(block):
        block_string = json.dumps(block,sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]


# app = Flask(__name__)
# node_identifier = str(uuid4()).replace('-','')
#
# # blockchain initializing
# blockchain = Blockchain()
# @app.route('/mine', methods = ['GET'])
# def mine():
#     last_block = blockchain.last_block
#     last_proof = last_block['proof']
#     proof = blockchain.proof_of_work(last_proof)
#
#     blockchain.new_transaction(
#     sender="0",
#     recipient = node_identifier,
#     amount = 1,
#     )
#
#     # now create the new block and add it to the chain
#     previous_hash = blockchain.hash(last_block)
#     block = blockchain.new_block(proof, previous_hash)
#
#     response = {
#         'message': 'The new block has been forged',
#         'index': block['index'],
#         'proof': block['proof'],
#         'previous_hash': block['previous_hash']
#     }
#
#     return jsonify(response), 200
#
# @app.route('/transactions/new', methods=['POST'])
# def new_transaction():
#     values = request.get_json()
#     # checking if the required data is there or not
#     required = ['sender', 'recipient', 'amount']
#     if not all(k in calues for k in required):
#         return 'Missing values', 400
#
#     index = blockchain.new_transaction(values['sender'], values['recipient', values['amount']])
#     response = {'message': f'Transaction is scheduled to be added to Block No.{index}'}
#     return jsonify(response), 201
#
# @app.route('/chain', methods=['GET'])
# def full_chain():
#     response = {
#         'chain': blockchain.chain,
#         'length': len(blockchain.chain)
#     }
#     return jsonify(response), 200
#
# if __name__=='__main__':
#     app.run(host="0.0.0.0", port=5000)
