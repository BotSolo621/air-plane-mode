import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import os
import requests
import logging

load_dotenv(".env")
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

def make_table(data, headers, col_widths=None):
    if col_widths is None:
        col_widths = []
        for i in range(len(headers)):
            max_len = len(headers[i])
            for row in data:
                if i < len(row):
                    max_len = max(max_len, len(str(row[i])))
            col_widths.append(max_len)

    tl, tm, tr = "┌", "┬", "┐"
    ml, mm, mr = "├", "┼", "┤"
    bl, bm, br = "└", "┴", "┘"
    h, v = "─", "│"

    def build_line(left, mid, right):
        line = left
        for i, w in enumerate(col_widths):
            line += h * (w + 2)
            line += mid if i < len(col_widths) - 1 else right
        return line

    header_cells = [f" {h.ljust(w)} " for h, w in zip(headers, col_widths)]
    header_row = v + v.join(header_cells) + v

    data_rows = []
    for row in data:
        row_cells = []
        for i, w in enumerate(col_widths):
            cell = str(row[i]) if i < len(row) else ""
            row_cells.append(f" {cell.ljust(w)} ")
        data_rows.append(v + v.join(row_cells) + v)

    table = [
        build_line(tl, tm, tr),
        header_row,
        build_line(ml, mm, mr),
        *data_rows,
        build_line(bl, bm, br),
    ]
    return "\n".join(table)

GUILD_ID = 1322767805782691942

@bot.event
async def on_ready():
    print("on_ready fired!")
    guild = discord.Object(id=GUILD_ID)
    await bot.tree.sync(guild=guild)
    print("[+] Guild commands synced!")

@bot.tree.command(name="cows", description="List all cows with status in a table")
async def listCows(interaction: discord.Interaction):
    await interaction.response.send_message("Fetching cows...")
    url = f"http://127.0.0.1:8000/command/listcows/"
    r = requests.get(url)
    data = r.json()
    cows = data.get("cows", [])
    if not cows:
        await interaction.edit_original_response(content="No cows present")
        return
    cow_data = [(cid, name, "Online" if cid.endswith("1") else "Offline") for cid, name in cows]
    headers = ["ID", "Name", "Status"]
    table_text = make_table(cow_data, headers)

    await interaction.edit_original_response(content=f"```\n{table_text}\n```")

@bot.tree.command(name="ssh", description="Remotely access the terminal of the cow")
@app_commands.describe(cow="cow's ID")
async def terminal(interaction: discord.Interaction, cow: str):
    await interaction.response.send_message("Creating ssh tunnel...")
    url = f"http://127.0.0.1:8000/command/ssh/{cow}"
    r = requests.get(url)
    data = r.json()
    if data.get("status") != "ok":
        await interaction.edit_original_response(content="Request failed.")
    await interaction.edit_original_response(content="```ssh user@serverip```")

print("Running...")
bot.run(token, log_handler=handler, log_level=logging.DEBUG)
