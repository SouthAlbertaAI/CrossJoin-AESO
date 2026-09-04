
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

from discord.ext.commands import Bot
import structlog as sl
from static import CrossJoin_Sys as Sys, CrossJoin_CommandLogic as CommandLogic
from dotenv import load_dotenv
from typing import Any

load_dotenv()

Log = sl.get_logger()


# Dispatch
def HotInfer(user_input: str, client: Bot, user_context: Any = None):
    match user_input:
        case "average":
            Log.info("Average command triggered")
            return CommandLogic.AveragePriceBasic(user_context)
        case "capacity":
            Log.info("Capacity command triggered")
            return CommandLogic.CapacityBasic()
        case "sources":
            Log.info("Sources command triggered")
            return CommandLogic.SourcesBasic(user_context)
        case "check-safe":
            Log.info("Check-Safe command triggered")
            return CommandLogic.CheckCapacityOverage(user_context)
        case "set-channel":
            Log.info("Set-Channel command triggered")
            return CommandLogic.GetChannelId(user_context, client)
        case "cams":
            Log.info("Camera command triggered")
            return CommandLogic.GetCams(user_context[0], user_context[1])
        case "help":
            Log.info("Help command triggered")
            return CommandLogic.SendHelp()
        case "roads":
            Log.info("Roads command triggered")
            return CommandLogic.GetRoadConditions(user_context)
        case "ping":
            Log.info("Ping command triggered")
            return CommandLogic.UserRequestedPing()
        case _:
            Log.info(f"Invalid command sent ({user_context}).")
            return Sys.ErrorMessage_Command("Not A Command.\nYou can find the command list with `!CrossJoin help`.")
