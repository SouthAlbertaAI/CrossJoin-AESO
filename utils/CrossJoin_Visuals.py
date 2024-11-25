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
    plt.legend(loc="upper left")
    plt.savefig("CacheFile.png")
    return Image.open("CacheFile.png").tobytes()
