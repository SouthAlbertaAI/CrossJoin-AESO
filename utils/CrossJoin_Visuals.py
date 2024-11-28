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
    plt.legend(loc="upper right")
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
