# module_1

import datetime
import hashlib
import json
from flask import Flask, jsonify #플라스크클래스라이브러리, 블록체인과상호작용할메세지를보내기위함

#제네시스블록:블록체인 다음의 첫번째블록생성
#
#

class Blockchain:

    #초기화
    def __init__(self):
        self.chain = [] # 블록체인의체인, 블록을포함한 체인,다른블록을포함한 리스트
        self.create_block(proof = 1, previous_hash = '0') #증명,이전해시 첫블록생성함수(제네시스)
    
    #제네시스블록생성함수
    def create_block(self, proof, previous_hash): #증명,이전해시
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    # 이전블록호출
    def get_previous_block(self):
        return self.chain[-1] # -1 마지막블록

    # 작업증명
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False: #올바른증명인지체크
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True