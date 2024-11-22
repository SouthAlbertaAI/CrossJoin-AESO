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

import requests as r
import datetime as dt
import structlog as sl
import json
import discord
from static import CrossJoin_Sys as Sys
import re
from dotenv import load_dotenv
import os


load_dotenv()

log = sl.get_logger()


# Commands are all managed here
def CheckCapacityOverage():
    try:
        headers = {
            "X-API-Key": os.getenv("API_KEY"),
            "content-type": "application/json"}
        return_text = r.get(
            f"https://api.aeso.ca/report/v1/csd/summary/current",
            headers=headers)
        return_text = json.loads(return_text.content)
        check = (float(return_text["return"]["alberta_internal_load"]) / float(return_text["return"]["total_max_generation_capability"])) * 100
        check = round(check, 2)
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f"Current Alberta Grid Load Stats",
            description=f"""
            Alberta Current Load Is Using This Percent Of Our Max Capacity: {check}%
            Alberta Current Load: {return_text["return"]["alberta_internal_load"]} Megawatts
            Alberta Current Max Generation Capacity: {return_text["return"]["total_max_generation_capability"]} Megawatts
            """,
            type="rich",
            timestamp=dt.datetime.now()
        )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Basic(str(e))


def AveragePriceBasic(user_input: str):
    flag = 0
    if "-" in user_input:
        extraction = re.search(r"\--(.*)", user_input)
        if extraction is not None:
            flag = 1
            extraction = extraction.group(1)
            extraction = extraction.strip("-")
            extraction = str(extraction)
    try:
        current_date = dt.date.today()
        if flag != 1:
            previous_date_default = current_date - dt.timedelta(days=7)
        else:
            previous_date_default = current_date - dt.timedelta(days=int(re.search(r"\d+",
                                                                                   extraction).group(0)))
        headers = {
            "X-API-Key": os.getenv("API_KEY"),
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
        if extraction is not None:
            true_days = extraction
        else:
            true_days = 7
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f"Average Price Over {true_days} Days",
            description=str(round(price_average_set_days, 2)),
            type="rich",
            timestamp=dt.datetime.now()
        )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Basic(str(e))


def CapacityBasic():
    try:
        headers = {
            "X-API-Key": os.getenv("API_KEY"),
            "content-type": "application/json"}
        return_text = r.get(
            f"https://api.aeso.ca/report/v1/csd/summary/current",
            headers=headers)
        return_text = json.loads(return_text.content)
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f"Current Alberta Grid Load Stats",
            description=f"""
            Alberta Current Power Usage(Megawatts): {return_text["return"]["alberta_internal_load"]}\n\n
            Alberta Current Power Generated(Megawatts): {return_text["return"]["total_net_generation"]}\n\n
            Alberta Max Generation Capacity(Megawatts): {return_text["return"]["total_max_generation_capability"]}\n\n
            """,
            type="rich",
            timestamp=dt.datetime.now()
        )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Basic(str(e))


def SourcesBasic():
    try:
        headers = {
            "X-API-Key": os.getenv("API_KEY"),
            "content-type": "application/json"}
        return_text = r.get(
            f"https://api.aeso.ca/report/v1/csd/generation/assets/current",
            headers=headers)
        return_text = json.loads(return_text.content)

        gas_true = 0
        stored_true = 0
        other_true = 0
        hydro_true = 0
        solar_true = 0
        wind_true = 0
        for z in return_text["return"]["asset_list"]:
            match z["fuel_type"].lower():
                case "gas":
                    gas_true += float(z["net_generation"])
                    gas_true += float(z["dispatched_contingency_reserve"])
                case "energy storage":
                    stored_true += float(z["net_generation"])
                    stored_true += float(z["dispatched_contingency_reserve"])
                case "other":
                    other_true += float(z["net_generation"])
                    other_true += float(z["dispatched_contingency_reserve"])
                case "hydro":
                    hydro_true += float(z["net_generation"])
                    hydro_true += float(z["dispatched_contingency_reserve"])
                case "solar":
                    solar_true += float(z["net_generation"])
                    solar_true += float(z["dispatched_contingency_reserve"])
                case "wind":
                    wind_true += float(z["net_generation"])
                    wind_true += float(z["dispatched_contingency_reserve"])
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f"Current Alberta Power Types Usage(Over 5 Megawatts)",
            description=f"""
            Gas Currently Used: {gas_true} Megawatts\n\n
            Other Fuel Types Currently Used: {other_true} Megawatts\n\n
            Stored Fuel Types Currently Used: {stored_true} Megawatts\n\n
            Hydro Fuel Types Currently Used: {hydro_true} Megawatts\n\n
            Solar Fuel Types Currently Used: {solar_true} Megawatts\n\n
            Wind Fuel Types Currently Used: {wind_true} Megawatts\n\n
            """,
            type="rich",
            timestamp=dt.datetime.now()
        )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Basic(str(e))


def GetChannelId(user_input: str, client: discord.Client):
    try:
        extraction = re.search(r"\--(.*)", user_input).group(1)
        client.channel_main = discord.utils.get(client.get_all_channels(), name=str(extraction)).id
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f"You have set the bot channel",
            description=f"""
            Bot Channel Configured As: #{extraction}
            Channel ID: {client.channel_main}
                    """,
            type="rich",
            timestamp=dt.datetime.now()
        )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Basic(str(e))


