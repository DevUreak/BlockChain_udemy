# module_1

import datetime
import hashlib
import json
from flask import Flask, jsonify #플라스크클래스라이브러리, 블록체인과상호작용할메세지를보내기위함

#제네시스 블록:블록 체인 다음의 첫 번째 블록 생성
#선행 제로 IDE는 채굴자들이 작업증명을찾기위한 문제를정의하는대표적인방법 (proof_of_work)
#선행 제로가 많아 질 수록 채굴자는 문제를 해결하기 더 여려워짐

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

    # 작업 증명 함수!
    # 여기서는 hash_opertaion 값이 0000으로 시작 하게 되면 
    # 확인 증명이 참 으로 변경 되고 채굴자는 성공을 하는걸로!
    # 그러나 선행제로가 0000으로 시작 하지 않는다면 채굴자는 
    # 값 을 올리면서 찾아볼 것 이므로 else에 아래 같은 로직을 넣는다
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False: #올바른증명인지체크, 채굴자가해결해야할문제
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':# 해시선행0000
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    # 블록해시화
    def hash(self, block): 
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    # 블록체인의유효성체크
    # 즉전체체인이블록들이이전해시들이현재같은지를검증하는것임
    # 첫번째는이전해시같은여부를확인하는것이고
    # 두번째는 자격증명이선행제로0000으로시작하는지검증하는것임
    # 결과적으로모두통과시다음체인검증으로넘어감
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