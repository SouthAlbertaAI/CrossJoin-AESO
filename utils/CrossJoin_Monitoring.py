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
from static import CrossJoin_Sys as cjs
from dotenv import load_dotenv
import os

load_dotenv()

Log = sl.get_logger()


def CheckCapacityOverage():
    try:
        headers = {
            "X-API-Key": os.getenv("API_KEY"),
            "content-type": "application/json"}
        return_text = r.get(
            f"https://api.aeso.ca/report/v1/csd/summary/current",
            headers=headers)
        return_text = json.loads(return_text.content)
        Check = (float(return_text["return"]["alberta_internal_load"]) / float(return_text["return"]["total_max_generation_capability"])) * 100
        Check = round(Check, 2)
        main_return = discord.Embed(
            colour=discord.Color.gold(),
            title=f"Current Alberta Grid Load Stats",
            description=f"""
            Alberta Current Load Is Using This Percent Of Our Max Capacity: {Check}%
            Alberta Current Load: {return_text["return"]["alberta_internal_load"]} Megawatts
            Alberta Current Max Generation Capacity: {return_text["return"]["total_max_generation_capability"]} Megawatts
            """,
            type="rich",
            timestamp=dt.datetime.now()
        )
        return main_return
    except Exception as e:
        Log.info(f"Error: Basic CrossJoin Run Failed. Reason: {e}")
        return cjs.ErrorMessage_Basic(str(e))
