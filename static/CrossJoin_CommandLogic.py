
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
from utils import CrossJoin_Visuals as Vis
import re
from dotenv import load_dotenv
import os
from textwrap import dedent
import shlex 


load_dotenv()

log = sl.get_logger()


# Commands are all managed here
def CheckCapacityOverage(user_input: str = None):
    flag = 0
    if "--" in user_input:
        extraction = re.search(r"\--(.*)", user_input)
        if extraction is not None:
            extraction = extraction.group(0)
            extraction = extraction.strip("-")
            extraction = str(extraction)
            if extraction == "visual":
                flag = 1
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
            title=f"Current Alberta Grid Load Stats",
            description=f"""
            Alberta Current Load Is Using This Percent Of Our Max Capacity: {check}%
            Alberta Current Load: {return_text["return"]["alberta_internal_load"]} Megawatts
            Alberta Current Max Generation Capacity: {return_text["return"]["total_max_generation_capability"]} Megawatts
            Alert Mode Triggered: {str(alert_mode_check)}
            """,
            type="rich",
            timestamp=dt.datetime.now()
        )
        if flag == 1:
            Vis.GraphReference(int(return_text["return"]["alberta_internal_load"]),
                               int(return_text["return"]["total_max_generation_capability"]))
            main_return.set_image(url="attachment://CacheFile.png")
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))


def AveragePriceBasic(user_input: str):
    flag = 0
    extraction = None
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
        return Sys.ErrorMessage_Command(str(e))


def SourcesBasic(user_input: str = None):
    flag = 0
    if "-" in user_input:
        extraction = re.search(r"\--(.*)", user_input)
        if extraction is not None:
            extraction = extraction.group(1)
            extraction = extraction.strip("-")
            extraction = str(extraction)
            if extraction == "visual":
                flag = 1
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

        gas_true = 0
        gas_overtime = []
        
        stored_true = 0
        stored_overtime = []

        other_true = 0
        other_overtime = []

        hydro_true = 0
        hydro_overtime = []

        solar_true = 0
        solar_overtime = []

        wind_true = 0
        wind_overtime = []
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
            title=f"Current Alberta Power Types Usage (Over 5 Megawatts)",
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

        if flag == 1:
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
        return Sys.ErrorMessage_Command(str(e))


def GetCams(user_input: str):
    try:
        if len(user_input.split()) < 3:
            main_return = discord.Embed(
                colour=0x00eaff,
                title=f"511 Alberta",
                description=dedent('''
                                You need to provide a search term. 
                                Please ensure this is wrapped in double quotes (").
                                Example: `!CrossJoin cams "Nose Hill Drive NW"`.
                                '''),
                type="rich",
                timestamp=dt.datetime.now()
            )
        else:
            userSearch = user_input.split('"')[1]
            userSplitWSearch = shlex.split(user_input)
            headers = {
                "content-type": "application/json"
            }
            return_text = r.get(
                "https://511.alberta.ca/api/v2/get/cameras?format=json&lang=en",
                headers=headers
            )
            return_text = json.loads(return_text.content)
            i = 0
            while i != len(return_text):
                if userSearch.lower() in return_text[i]["Location"].lower():
                    x = return_text[i]
                    t = str(dt.datetime.now())
                    for i in [':', ' ', '.', '-']:
                        t = t.replace(i, "")
                    if len(userSplitWSearch) < 4  or int(userSplitWSearch[3]) < 1:
                        cameraNum = 0
                    elif int(userSplitWSearch[3]) > len(x['Views']):
                        cameraNum = len(x["Views"]) - 1
                    else:
                        cameraNum = int(userSplitWSearch[3]) - 1
                    main_return = discord.Embed(
                        colour=0x00eaff,
                        title=f"511 Alberta > {x['Location']}",
                        description=dedent(f"""
                        {x['Views'][cameraNum]['Description']}.
                        - Direction: {x['Direction']}.
                        - Position: {x['Latitude']}, {x['Longitude']}.
                        -# This location has {len(x['Views'])} camera(s). 
                        -# Specify a specific camera with `!CrossJoin cams [1-{len(x['Views'])}]`.
                        """),
                        type="rich",
                        timestamp=dt.datetime.now()
                    )
                    main_return.set_image(url=x['Views'][cameraNum]["Url"].replace(" ", "%20") + f"?t={t}")
                    break
                i += 1
            else:
                main_return = discord.Embed(
                    colour=0x00eaff,
                    title=f"511 Alberta > {userSearch}",
                    description=dedent("""
                    The search yielded no results.
                    """),
                    type="rich",
                    timestamp=dt.datetime.now()
                )
        return main_return
    except Exception as e:
        log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return Sys.ErrorMessage_Command(str(e))


def GetRoadConditions(user_input: str = None):
    extraction = "Calgary"
    if "--" in user_input:
        extraction = re.search(r"\--(.*)", user_input)
        if extraction is not None:
            extraction = extraction.group(1)
            extraction = extraction.strip("-")
            extraction = str(extraction)
            if extraction == "":
                extraction = "Calgary"
    headers = {
        "content-type": "application/json"
    }
    return_text = r.get(
        "https://511.alberta.ca/api/v2/get/winterroads?format=json&lang=en",
        headers=headers
    )
    return_text = json.loads(return_text.content)
    VisibilityMain = []
    RoadConditionsMain = []
    RoadConditionsSecondary = []
    for z in return_text:
        try:
            if extraction in z["LocationDescription"]:
                RoadConditionsMain.append(z["Primary Condition"])
                VisibilityMain.append(z["Visibility"])
                for k in z["Secondary Conditions"]:
                    RoadConditionsSecondary.append(k)
        except Exception as e:
            log.info(f"Attempt To Access Road Condition Record Failed. Reason {e}")

    main_return = discord.Embed(
        colour=discord.Colour.gold(),
        title=f"Road Reports For The {extraction} Area",
        description=f"""
            **Main Conditions**
            The Main reported road conditions in {extraction} are: {max(RoadConditionsMain, key=RoadConditionsMain.count)}\n
            Road visibility is reported as: {max(VisibilityMain, key=VisibilityMain.count)}
            
            
            **Secondary Conditions**
            """,
        type="rich",
        timestamp=dt.datetime.now()
    )

    if len(RoadConditionsSecondary) > 0:
        ElementPassOne = RoadConditionsSecondary[0]
        main_return.description += f"""Secondary road conditions have also been reported as follows:
                - {ElementPassOne}\n
                """
        if len(RoadConditionsSecondary) > 1:
            ElementPassTwo = RoadConditionsSecondary[1]
            main_return.description += f"- {ElementPassTwo}"
    else:
        main_return.description += "There is no notable secondary road conditions to note."

    return main_return


def SendHelp(user_input: str = None):
    try:
        cmdPrefix = "!CrossJoin"
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f"CrossJoin Command Syntax",
            description=dedent(f"""
            - `{cmdPrefix} average` - Shows the average price over a specified amount of days.
            - `{cmdPrefix} capacity` - Shows stats about capacity and load of Alberta's power grid.
            - `{cmdPrefix} sources` - Search a source for information.
            - `{cmdPrefix} check-safe` - Checks grid usage to see if its overcapacity. 
            - `{cmdPrefix} set-channel` - Sets a specific channel to post updates. 
            - `{cmdPrefix} cams` - Gets cameras from [Alberta 511](https://511.alberta.ca).
            - `{cmdPrefix} help` - Shows this message.
            -# Built by [SouthAlbertaAI](https://github.com/SouthAlbertaAI) and [contributors](https://github.com/SouthAlbertaAI/CrossJoin-AESO/graphs/contributors).
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
    print("Skeleton For Now")


GetRoadConditions("!CrossJoin roads")
