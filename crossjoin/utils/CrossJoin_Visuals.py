
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

import matplotlib.pyplot as plt
from PIL import Image


# For sources
def GraphSources(XAxisName: str, YAxisName: str, Data: list, Data2: list):
    fig, ax = plt.subplots()
    Count = 0
    for z in Data:
        ax.plot(z, label=Data2[Count])
        Count += 1
    plt.xlabel(XAxisName)
    plt.ylabel(YAxisName)
    plt.legend(loc="upper right", title="Power Types")
    plt.savefig("CacheFile.png")
    return Image.open("CacheFile.png").tobytes()


def GraphReference(CurrentPowerUsage: int, MaxGeneration: int):
    fix, ax = plt.subplots()
    DangerZone = (0.8 * (MaxGeneration))
    ax.plot([CurrentPowerUsage, CurrentPowerUsage], label="Current Power Usage")
    ax.plot([MaxGeneration, MaxGeneration], label="Max Power Capacity")
    ax.plot([DangerZone, DangerZone], label="Danger Zone")
    plt.ylim(bottom=5000)
    plt.legend(loc="upper right")
    plt.xlabel("Power Thresholds")
    plt.ylabel("Power Usage Megawatts")
    plt.savefig("CacheFile.png")
    return Image.open("CacheFile.png").tobytes()