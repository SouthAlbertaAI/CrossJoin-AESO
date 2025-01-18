
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
import datetime

import requests as r
import datetime as dt
import structlog as sl
import json
import discord
from static import CrossJoin_Sys as Sys
from utils import CrossJoin_Visuals as Vis
import re
from dotenv import load_dotenv
import os
from textwrap import dedent
from fuzzywuzzy import process
from PIL import Image
import urllib.request
import shlex # this import is only for unix systems, making it platform dependant. 


load_dotenv()

log = sl.get_logger()


def CheckCapacityOverage(user_input: bool):
    try:
        headers = {
            "X-API-Key": os.getenv("AESO_API_KEY"),
            "content-type": "application/json"}
        return_text = r.get(
            f"https://api.aeso.ca/report/v1/csd/summary/current",
            headers=headers)
        return_text = json.loads(return_text.content)
        check = (float(return_text["return"]["alberta_internal_load"]) / float(return_text["return"]["total_max_generation_capability"])) * 100
        check = round(check, 2)
        if float(return_text["return"]["alberta_internal_load"]) >= (float(return_text["return"]["total_max_generation_capability"]) * 0.8):
            alert_mode_check = True
        else:
            alert_mode_check = False
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f":factory::zap: Current Alberta Grid Load Stats",
            description=dedent(f"""
            - Alberta Current Load Is Using This Percent Of Our Max Capacity: {check}%
            - Alberta Current Load: {return_text["return"]["alberta_internal_load"]} MW
            - Alberta Current Max Generation Capacity: {return_text["return"]["total_max_generation_capability"]} MW
            - Alert Mode Triggered: {str(alert_mode_check)}
            """),
            type="rich",
            timestamp=dt.datetime.now()
        )
        if user_input is True:
            Vis.GraphReference(int(return_text["return"]["alberta_internal_load"]),
                               int(return_text["return"]["total_max_generation_capability"]))
            main_return.set_image(url="attachment://CacheFile.png")
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))


def AveragePriceBasic(days: int = 7):
    try:
        current_date = dt.date.today()
        previous_date_default = current_date - dt.timedelta(days=days)
        headers = {
            "X-API-Key": os.getenv("AESO_API_KEY"),
            "content-type": "application/json"}
        return_text = r.get(
            f"https://api.aeso.ca/report/v1.1/price/poolPrice?startDate={previous_date_default}&endDate={current_date}",
            headers=headers)
        return_text = json.loads(return_text.content)
        price_average_set_days = 0.0
        true_count = 0
        for z in return_text["return"]["Pool Price Report"]:
            try:
                price_average_set_days += float(z["pool_price"])
                true_count += 1
            except Exception as e:
                log.info(f"Error in data analysis: {e}")
                price_average_set_days += 0.0
        price_average_set_days = price_average_set_days / true_count
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f":factory::zap: Average Price Over {days} Days",
            description=f"**${str(round(price_average_set_days, 2))}**",
            type="rich",
            timestamp=dt.datetime.now()
        )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))


def CapacityBasic():
    try:
        headers = {
            "X-API-Key": os.getenv("AESO_API_KEY"),
            "content-type": "application/json"}
        return_text = r.get(
            f"https://api.aeso.ca/report/v1/csd/summary/current",
            headers=headers)
        return_text = json.loads(return_text.content)
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f":factory::zap: Current Alberta Grid Load Stats",
            description=dedent(f"""
            - Alberta Current Power Usage: {return_text["return"]["alberta_internal_load"]} MW
            - Alberta Current Power Generated: {return_text["return"]["total_net_generation"]} MW
            - Alberta Max Generation Capacity: {return_text["return"]["total_max_generation_capability"]} MW
            """),
            type="rich",
            timestamp=dt.datetime.now()
        )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))


def SourcesBasic(user_input: bool):
    try:
        headers = {
            "X-API-Key": os.getenv("AESO_API_KEY"),
            "content-type": "application/json"}
        return_text = r.get(
            f"https://api.aeso.ca/report/v1/csd/generation/assets/current",
            headers=headers)
        return_text = json.loads(return_text.content)

        data_main = []
        data_main_2 = ["gas", "stored", "other", "hydro", "solar", "wind"]

        gas_true = 0 ;    gas_overtime = []
        stored_true = 0 ; stored_overtime = []
        other_true = 0 ;  other_overtime = []
        hydro_true = 0 ;  hydro_overtime = []
        solar_true = 0 ;  solar_overtime = []
        wind_true = 0 ;   wind_overtime = []

        for z in return_text["return"]["asset_list"]:
            match z["fuel_type"].lower():
                case "gas":
                    gas_true += float(z["net_generation"])
                    gas_true += float(z["dispatched_contingency_reserve"])
                    gas_overtime.append(float(z["net_generation"]))
                case "energy storage":
                    stored_true += float(z["net_generation"])
                    stored_true += float(z["dispatched_contingency_reserve"])
                    stored_overtime.append(float(z["net_generation"]))
                case "other":
                    other_true += float(z["net_generation"])
                    other_true += float(z["dispatched_contingency_reserve"])
                    other_overtime.append(float(z["net_generation"]))
                case "hydro":
                    hydro_true += float(z["net_generation"])
                    hydro_true += float(z["dispatched_contingency_reserve"])
                    hydro_overtime.append(float(z["net_generation"]))
                case "solar":
                    solar_true += float(z["net_generation"])
                    solar_true += float(z["dispatched_contingency_reserve"])
                    solar_overtime.append(float(z["net_generation"]))
                case "wind":
                    wind_true += float(z["net_generation"])
                    wind_true += float(z["dispatched_contingency_reserve"])
                    wind_overtime.append(float(z["net_generation"]))
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f":factory::zap: Current Alberta Power Types Usage (Over 5 MW)",
            description=dedent(f"""
            - :fire: Gas Currently Used: {gas_true} MW
            - :regional_indicator_o: Other Fuel Types Currently Used: {other_true} MW
            - :regional_indicator_s: Stored Fuel Types Currently Used: {stored_true} MW
            - :ocean: Hydro Fuel Types Currently Used: {hydro_true} MW
            - :high_brightness: Solar Fuel Types Currently Used: {solar_true} MW
            - :cyclone: Wind Fuel Types Currently Used: {wind_true} MW
            """),
            type="rich",
            timestamp=dt.datetime.now()
        )

        if user_input is True:
            data_main.append(gas_overtime)
            data_main.append(stored_overtime)
            data_main.append(other_overtime)
            data_main.append(hydro_overtime)
            data_main.append(solar_overtime)
            data_main.append(wind_overtime)

            Vis.GraphSources("Power Producing Assets", "Power Produced(Megawatts)",
                             data_main, data_main_2)
            main_return.set_image(url="attachment://CacheFile.png")
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))


def GetChannelId(user_input: str, client: discord.Client):
    try:
        client.channel_main = discord.utils.get(client.get_all_channels(), name=user_input).id
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f"You have set the bot channel",
            description=f"""
            Bot Channel Configured As: #{user_input}
            Channel ID: {client.channel_main}
                    """,
            type="rich",
            timestamp=dt.datetime.now()
        )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))


def GetCams(user_input: str, cam_specifier: int = 1):
    try:
        headers = {
            "content-type": "application/json"
        }
        return_text = r.get(
            "https://511.alberta.ca/api/v2/get/cameras?format=json&lang=en",
            headers=headers
        )
        return_text = json.loads(return_text.content)
        true_list = [z["Location"] for z in return_text]
        true_list_dict = {idx: z for idx, z in enumerate(true_list)}
        high_matches = process.extract(user_input, true_list_dict, limit=5)
        usage = return_text[high_matches[0][2]]
        if len(usage["Views"]) > 1 and cam_specifier <= len(usage["Views"]) - 1:
            main_image = usage["Views"][cam_specifier]["Url"]
        else:
            main_image = usage["Views"][0]["Url"]
        img_name = "MainImage.png"
        urllib.request.urlretrieve(main_image, img_name)
        main_return = discord.Embed(
            colour=0x00eaff,
            title=f":red_car: 511 Alberta - {usage['Location']}",
            description=dedent(f'''
                                    {usage["Views"][0]["Description"]}.
                                    - Direction: {usage["Direction"]}.
                                    - Position: {usage["Latitude"]}, {usage["Longitude"]}.
                                    -# This location has {len(usage["Views"])} camera(s). 
                                    -# Specify a specific camera with `!CrossJoin cams "[Location]" [1-{len(usage["Views"])}]`.
                                    '''),
            type="rich",
            timestamp=dt.datetime.now()
        )
        main_return.set_image(url="attachment://MainImage.png")
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))


def GetCams(user_input: str, cam_specifier: int = 1):
    try:
        headers = {
            "content-type": "application/json"
        }
        return_text = r.get(
            "https://511.alberta.ca/api/v2/get/cameras?format=json&lang=en",
            headers=headers
        )
        return_text = json.loads(return_text.content)
        true_list = [z["Location"] for z in return_text]
        true_list_dict = {idx: z for idx, z in enumerate(true_list)}
        high_matches = process.extract(user_input, true_list_dict, limit=5)
        usage = return_text[high_matches[0][2]]
        cam_specifier -= 1
        comparison = usage["Views"]
        comparison = int(len(comparison))
        if 0 <= cam_specifier <= (comparison - 1):
            main_image = usage["Views"][cam_specifier]["Url"]
        else:
            main_image = usage["Views"][0]["Url"]
        img_name = "MainImage.png"
        urllib.request.urlretrieve(main_image, img_name)
        main_return = discord.Embed(
            colour=0x00eaff,
            title=f":red_car: 511 Alberta - {usage['Location']}",
            description=dedent(f'''
                                    {usage["Views"][0]["Description"]}.
                                    - Direction: {usage["Direction"]}.
                                    - Position: {usage["Latitude"]}, {usage["Longitude"]}.
                                    -# This location has {len(usage["Views"])} camera(s). 
                                    -# Specify a specific camera with `!CrossJoin cams "[Location]" [1-{len(usage["Views"])}]`.
                                    '''),
            type="rich",
            timestamp=dt.datetime.now()
        )
        main_return.set_image(url="attachment://MainImage.png")
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))
        

def UserRequestedPing(user_input: str = None):
    try:
        main_return = discord.Embed(
            colour=discord.Color.greyple(),
            title=f":interrobang: Ping Requested",
            description=dedent(f"""
                `PONG!` :incoming_envelope::gear: `PONG!`
                `PONG!` :incoming_envelope::gear: `PONG!`
                `PONG!` :incoming_envelope::gear: `PONG!`
            """),
            type="rich",
            timestamp=dt.datetime.now()
            )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))

def SendHelp(user_input: str = None):
    try:
        main_return = discord.Embed(
            colour=discord.Color.greyple(),
            title=f":interrobang: CrossJoin Command Syntax",
            description=dedent(f"""
            - `average` - Shows the average price over a specified amount of days.
            - `capacity` - Shows stats about capacity and load of Alberta's power grid.
            - `sources` - Search a source for information.
            - `check-safe` - Checks grid usage to see if its overcapacity. 
            - `set-channel` - Sets a specific channel to post updates. 
            - `cams` - Gets cameras from [Alberta 511](https://511.alberta.ca).
            - `roads` - Gets current road conditions as reported from [Alberta 511](https://511.alberta.ca).
            - `help` - Shows this message.
            -# Built by [SouthAlbertaAI](https://github.com/SouthAlbertaAI) and [contributors](https://github.com/SouthAlbertaAI/CrossJoin-AESO/graphs/contributors).
            """),
            type="rich",
            timestamp=dt.datetime.now()
        )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))


def UserRequestedPing():
    try:
        main_return = discord.Embed(
            colour=discord.Color.greyple(),
            title=f":interrobang: Ping Requested",
            description=dedent(f"""
                `PONG!` :incoming_envelope::gear: `PONG!`
                `PONG!` :incoming_envelope::gear: `PONG!`
                `PONG!` :incoming_envelope::gear: `PONG!`
            """),
            type="rich",
            timestamp=dt.datetime.now()
            )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))


# Here as a skeleton for future implementation
def AlertMode():
    log.info("Skeleton For Now")
