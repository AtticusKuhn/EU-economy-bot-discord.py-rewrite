import discord
from config import config
from datetime import date

def simple_embed(success,message):
    if success=="info":
        color=0x0000ff
    if success:
        color=0x00ff00
    if not success:
        color=0xff0000
    if len(message)>2000:
        message=message[:2000]+"...."
    embedVar = discord.Embed(
        title="EU Economy Bot",
        description=message,
        color=color,
        url=config["website"]
    )
    embedVar.set_footer(text="A general purpose economy bot", icon_url=config["image"])
    return embedVar
def dict_to_embed(dict, image=None):
    embedVar = discord.Embed(
        title="Con bot",
        color=0x00ff00,
        url=config["website"]
    )
    for key, value in dict.items():
        if value == None or value=="":
            value="(none)"
        embedVar.add_field(name=key, value= value)
    embedVar.set_footer(text="A general purpose CoN bot", icon_url=config["image"])
    if image is not None:
        embedVar.set_image(url=image)
    return embedVar
