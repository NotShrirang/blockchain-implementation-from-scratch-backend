from blocks import Blockchain
from fastapi import FastAPI
from fastapi.responses import JSONResponse

description = """
Blockchain Simulation API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="Blockchain API",
    description=description,
    summary="Satoshi's favorite app. Nuff said.",
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Deadpoolio the Amazing",
        "url": "http://x-force.example.com/contact/",
        "email": "dp@x-force.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

blockchain = Blockchain()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/mine_block")
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
 
    response = {'message': 'A block is MINED',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
 
    return JSONResponse(response, 200)
 
@app.get('/get_chain')
async def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return JSONResponse(response, 200)

@app.get('/valid')
async def valid():
    valid = blockchain.chain_valid(blockchain.chain)
 
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return JSONResponse(response, 200)

@app.get('/display_blockchain')
async def display_blockchain():
    return JSONResponse(blockchain.display_chain(), 200)

@app.post('/add_block')
async def add_block(data: dict):
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    data = data['data']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash, data)
    return JSONResponse(block, 201)