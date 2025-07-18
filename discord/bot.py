import discord
from discord.ext import commands
from discord import app_commands
import logging
from dotenv import load_dotenv
import os
import requests

# Token
load_dotenv(dotenv_path=".env")
token = os.getenv('DISCORD_TOKEN')
apiToken = os.getenv('API_SECRET')

# Log stuff
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
intents = discord.Intents.default()
intents.message_content = True

# Bot commands
bot = commands.Bot(command_prefix='!', intents=intents)

def make_table(data, headers, col_widths=None):
    # data = list of tuples (id, name, status)
    # headers = list of header names
    # col_widths = list of int widths or None (auto calc)
    
    # Auto calc column widths if not provided
    if col_widths is None:
        # For each col, max length between header and data
        col_widths = []
        for col_idx in range(len(headers)):
            max_len = len(headers[col_idx])
            for row in data:
                if col_idx < len(row):
                    max_len = max(max_len, len(str(row[col_idx])))
            col_widths.append(max_len)
    
    # Box drawing chars
    top_left, top_mid, top_right = '┌', '┬', '┐'
    mid_left, mid_mid, mid_right = '├', '┼', '┤'
    bottom_left, bottom_mid, bottom_right = '└', '┴', '┘'
    horiz = '─'
    vert = '│'
    
    def build_line(left, mid, right):
        line = left
        for i, w in enumerate(col_widths):
            line += horiz * (w + 2)
            line += mid if i < len(col_widths) -1 else right
        return line
    
    # Build header row
    header_cells = []
    for h, w in zip(headers, col_widths):
        header_cells.append(f" {h.ljust(w)} ")
    header_row = vert + vert.join(header_cells) + vert
    
    # Build data rows
    data_rows = []
    for row in data:
        row_cells = []
        for i, w in enumerate(col_widths):
            cell = str(row[i]) if i < len(row) else ''
            row_cells.append(f" {cell.ljust(w)} ")
        data_rows.append(vert + vert.join(row_cells) + vert)
    
    # Assemble all parts
    table = []
    table.append(build_line(top_left, top_mid, top_right))
    table.append(header_row)
    table.append(build_line(mid_left, mid_mid, mid_right))
    table.extend(data_rows)
    table.append(build_line(bottom_left, bottom_mid, bottom_right))
    
    return "\n".join(table)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready!")
    await bot.tree.sync()

@bot.tree.command(name="cows", description="List all cows with status in a nice table")
async def listCows(interaction: discord.Interaction):
    await interaction.response.send_message("Listing all cows...")

    url = f"http://127.0.0.1:8000/command/listcows/{apiToken}"
    r = requests.get(url)
    data = r.json()

    if data.get("auth") != "ok":
        await interaction.edit_original_response(content="❌ Failed to authenticate, please DM eppybot")
        return

    cow_list = data.get("cows", [])
    if not cow_list:
        await interaction.edit_original_response(content="No cows connected....")
        return

    # Example: Add dummy status (replace with real status if you have it)
    cow_data_with_status = [(cid, name, "Online" if cid.endswith("1") else "Offline") for cid, name in cow_list]

    headers = ["ID", "Name", "Status"]
    table_text = make_table(cow_data_with_status, headers)

    await interaction.edit_original_response(content=f"```\n{table_text}\n```")

bot.run(token, log_handler=handler, log_level=logging.DEBUG)
