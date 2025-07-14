#Handle requests from both bot and client
#Stores commands and sends them
# Client sends : and bot sends !
from fastapi import FastAPI

app = FastAPI()

connected_devices = {}

#check if command exist for device, if so, send request.
#client
@app.get(":ping")
async def ping():
    

#server
@app.get("+listclient")
async def listclient():
    return {"msg": "pong"}