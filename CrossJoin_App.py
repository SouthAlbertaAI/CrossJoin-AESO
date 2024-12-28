
"""
The Clear BSD License

Copyright (c) 2024 SouthAlbertaAI
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted (subject to the limitations in the disclaimer
below) provided that the following conditions are met:

     * Redistributions of source code must retain the above copyright notice,
     this list of conditions and the following disclaimer.

     * Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

     * Neither the name of the copyright holder nor the names of its
     contributors may be used to endorse or promote products derived from this
     software without specific prior written permission.

NO EXPRESS OR IMPLIED LICENSES TO ANY PARTY'S PATENT RIGHTS ARE GRANTED BY
THIS LICENSE. THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""

import discord
from utils.CrossJoin_Main import CrossJoin
from utils.CrossJoin_Support import HotInfer
import structlog as sl
from dotenv import load_dotenv
import os

load_dotenv()

log = sl.get_logger()

# Run the app itself here, setup class instance
intents = discord.Intents.default()
intents.message_content = True
client = CrossJoin(intents=intents, command_prefix="!CrossJoin")
tree = client.tree


# Also still look into managing this as a separate class object
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
async def get_sources(interaction: discord.Interaction, visual: str = "None"):
    try:
        Response = HotInfer("sources", client, visual)
        Responder = interaction.response
        if Response.image.url is not None and Response.image.url.split(":")[0] == "attachment":
            await Responder.send_message(embed=Response,
                                         file=discord.File(Response.image.url.strip("attachment://")))
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
async def capacity_robust(interaction: discord.Interaction, visual: str = "None"):
    try:
        Response = HotInfer("check-safe", client, visual)
        Responder = interaction.response
        if Response.image.url is not None and Response.image.url.split(":")[0] == "attachment":
            await Responder.send_message(embed=Response,
                                         file=discord.File(Response.image.url.strip("attachment://")))
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
    description="A slightly more robust power usage command. This is also used to monitor alert mode.",
    nsfw=False
)
@discord.app_commands.describe(
    cam_name="The name of the camera you are looking for. If not exact it will look for closest match."
)
async def get_road_cams(interaction: discord.Interaction, cam_name: str):
    try:
        Response = HotInfer("cams", client, cam_name)
        Responder = interaction.response
        if Response.image.url is not None and Response.image.url.split(":")[0] == "attachment":
            hand_in = Response.image.url
            hand_in = hand_in.strip("attachment")
            hand_in = hand_in.strip("://")
            await Responder.send_message(embed=Response,
                                         file=discord.File(hand_in))
        else:
            await Responder.send_message(embed=Response)
    except Exception as e:
        log.info(f"Error In Road Cams Command {e}")


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
        log.info(f"Error In Get Help Command {e}")


client.run(os.getenv("DISCORD_KEY"))
