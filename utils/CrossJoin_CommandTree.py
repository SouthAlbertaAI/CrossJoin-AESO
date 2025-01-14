from CrossJoin_App import tree
from utils.CrossJoin_Support import HotInfer
import discord
import discord.ext
from CrossJoin_App import client
from CrossJoin_App import log
import os


# This is kept here for future and cleaner class implementation
@tree.command(
    name="average",
    description="check the average power price. Optionally specify amount of days.",
    nsfw=False,
)
@discord.app_commands.describe(
    days="The amount of days you want the command to encompass."
)
async def get_average_power_price(interaction: discord.Interaction, days: int):
    try:
        Response = HotInfer("average", client, days)
        Responder = interaction.response
        await Responder.send_message(embed=Response)
    except Exception as e:
        log.info(f"Error In Average Command {e}")


@tree.command(
    name="capacity",
    description="Provide some basic statistics on grid capacity and current usage.",
    nsfw=False,
)
async def get_basic_capacity(interaction: discord.Interaction):
    try:
        Response = HotInfer("capacity", client)
        Responder = interaction.response
        await Responder.send_message(embed=Response)
    except Exception as e:
        log.info(f"Error In Basic Capacity Command {e}")


@tree.command(
    name="sources",
    description="Get details on the amount of power being produced by different resource types.",
    nsfw=False
)
@discord.app_commands.describe(
    visual="Optionally, specify if you want a visual chart produced along with this output."
)
async def get_sources(interaction: discord.Interaction, visual: bool = True):
    try:
        Response = HotInfer("sources", client, visual)
        Responder = interaction.response
        if Response.image.url is not None and Response.image.url.split(":")[0] == "attachment":
            await Responder.send_message(embed=Response,
                                         file=discord.File(Response.image.url.strip("attachment://")))
            os.remove(Response.image.url.strip("attachment://"))
        else:
            await Responder.send_message(embed=Response)
    except Exception as e:
        log.info(f"Error In Sources Command {e}")


@tree.command(
    name="check-safe",
    description="A slightly more robust power usage command. This is also used to monitor alert mode.",
    nsfw=False
)
@discord.app_commands.describe(
    visual="Optionally, specify if you want a visual chart produced along with this output."
)
async def capacity_robust(interaction: discord.Interaction, visual: bool = True):
    try:
        Response = HotInfer("check-safe", client, visual)
        Responder = interaction.response
        if Response.image.url is not None and Response.image.url.split(":")[0] == "attachment":
            await Responder.send_message(embed=Response,
                                         file=discord.File(Response.image.url.strip("attachment://")))
            os.remove(Response.image.url.strip("attachment://"))
        else:
            await Responder.send_message(embed=Response)
    except Exception as e:
        log.info(f"Error In Advanced Capacity Command {e}")


@tree.command(
    name="set-channel",
    description="A slightly more robust power usage command. This is also used to monitor alert mode.",
    nsfw=False
)
@discord.app_commands.describe(
    channel="Set the channel for the discord bot, this allows for scheduled capacity checks and automatic alerts to run."
)
async def set_channel(interaction: discord.Interaction, channel: str):
    try:
        Response = HotInfer("set-channel", client, channel)
        Responder = interaction.response
        await Responder.send_message(embed=Response)
    except Exception as e:
        log.info(f"Error In Set Channel {e}")


@tree.command(
    name="cams",
    description="Gets the road camera view of the road that you specify. Optionally, specify specific cam number.",
    nsfw=False
)
@discord.app_commands.describe(
    cam_name="The name of the camera you are looking for. If not exact it will look for closest match.",
    cam_number="Optional command to specify which camera number you would like to check at the location."
)
async def get_road_cams(interaction: discord.Interaction, cam_name: str, cam_number: int = 1):
    try:
        Response = HotInfer("cams", client, [cam_name, cam_number])
        Responder = interaction.response
        if Response.image.url is not None and Response.image.url.split(":")[0] == "attachment":
            await Responder.send_message(embed=Response,
                                         file=discord.File("MainImage.png"))
            os.remove("MainImage.png")
        else:
            await Responder.send_message(embed=Response)
    except Exception as e:
        log.info(f"Error In Road Cams Command {e}")


@tree.command(
    name="roads",
    description="Get information on road conditions in a specific area.",
    nsfw=False
)
@discord.app_commands.describe(
    area="The area/city in which you would like details on the road conditions on."
)
async def get_roads(interaction: discord.Interaction, area: str):
    try:
        Response = HotInfer("roads", client, area)
        Responder = interaction.response
        await Responder.send_message(embed=Response)
    except Exception as e:
        log.info(f"Error In Get Roads Command {e}")


@tree.command(
    name="help",
    description="Get help on how to run the commands that are a part of this bot.",
    nsfw=False
)
async def get_help(interaction: discord.Interaction):
    try:
        Response = HotInfer("help", client)
        Responder = interaction.response
        await Responder.send_message(embed=Response)
    except Exception as e:
        log.info(f"Error In Get Help Command {e}")
