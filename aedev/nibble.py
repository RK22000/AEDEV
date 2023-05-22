import matplotlib.pyplot as plt
from typing import Tuple, List, Dict, Iterable
from itertools import chain
import random
import math
import os
import json
import sys

def nibble_distribution(file: str, figsize: Tuple[int, int] = (12, 5)) -> None:
    nib0: int = 240
    nib1: int = 15
    with open(file=file, mode='rb') as f:
        fbytes: bytes = f.read()
    map0: dict[int, int] = {i: 0 for i in range(15)}
    map1: dict[int, int] = {i: 0 for i in range(15)}
    for byte in fbytes:
        map0[(byte&nib0)>>4] = map0.setdefault((byte&nib0)>>4,0) + 1
        map1[byte&nib1] = map1.setdefault(byte&nib1, 0) + 1
    plt.figure(figsize=figsize)
    plt.subplot(121)
    plt.bar([i for i in map0], map0.values())
    plt.title("Distribution of first nibble")
    for x in map0:
        plt.text(x, map0[x], str(map0[x]), horizontalalignment='center')
    plt.subplot(122)
    plt.title("Distribution of second nibble")
    plt.bar([i for i in map1], map1.values())
    for x in map1:
        plt.text(x, map1[x], str(map1[x]), horizontalalignment='center')



# Nib1 prior
def prior_nib_prob(files: List[str]) -> Dict[int, Tuple[Tuple[int], Tuple[float]]]:
    nib0: int = 240
    nib1: int = 15
    counts: dict[int, dict[int, list[int]]] = {}
    for file in files:
        with open(file=file, mode='rb') as f:
            fbytes = f.read()
        for byte in fbytes:
            key = byte & nib1
            val = (byte & nib0) >> 4
            counts.setdefault(key, {}).setdefault(val, [0])[0]+=1

    probs: dict[int, tuple[tuple[int], tuple[float]]] = {}
    for byte in counts:
        prior_bytes, prior_counts = [[i for i in counts[byte]], [i[0] for i in counts[byte].values()]]
        tot = sum(prior_counts)
        probs[byte] = (tuple(prior_bytes), tuple([i for i in map(lambda i: i/tot, prior_counts)]))
    
    return probs

def save_probs(probs: Dict[int, Tuple[Tuple[int], Tuple[float]]], saveFileName: str) -> None:
    ps = probs
    jsn = json.dumps(ps)
    with(open(saveFileName, "w")) as f:
        f.write(jsn)

def load_probs(saveFileName: str) -> dict:
    if not os.path.isfile(saveFileName):
        print("File not found: ", sys.stderr)
        exit(2)
    with(open(saveFileName, "r")) as f:
        jsn = json.load(f)
    js = {int(key): jsn[key] for key in jsn.keys()}
    return js

            
# Function to get entropy of a list of bytes
def entropy(block: bytes, n: int) -> float:
    byte_map: dict[int, int] = {}
    for byte in block:
        byte_map[byte] = byte_map.setdefault(byte, 0) + 1
    probs = map(lambda x: float(x)/n, byte_map.values())
    entropies = map(lambda p: -p*math.log2(p), probs)
    return sum(entropies)

# Function to display entropy of a file given a specified window size
def file_entropy(file: str, window_size: int, label: str = "") -> None:
    entropies: list[float] = [0.0]
    with open(file=file, mode='rb') as f:
        while True:
            block = f.read(window_size)
            if block==bytes(): break
            #print(block)
            entropies.append(entropy(block=block, n=window_size))
            #print(entropies[-1])
    if label == "":
        label = f"window={window_size}" 
    plt.plot(range(len(entropies)), entropies, label=label)
    #print(entropies)

def file_analyze(
    benign_file: str, 
    encrypted_file: str = "", 
    masked_file: str = "", 
    sizes = range(10, 40, 8), 
    plt_size: Tuple[int, int] = (8, 6)
    ) -> None:
    """---"""
    
    col = 1 if encrypted_file=="" else 2
    col = col if masked_file=="" else 3
    plt_size = (8, 6)
    plt.figure(figsize=(plt_size[0]*col, plt_size[1]))
    
    plt.subplot(1, col, 1)
    for size in sizes:
        file_entropy(file=benign_file, window_size=size)
    plt.legend()
    plt.title("Unencrypted Entropy")
    if (col >= 2):
        plt.subplot(1, col, 2)
        for size in sizes:
            file_entropy(file=encrypted_file, window_size=size)
        plt.legend()
        plt.title("Encrypted Entropy")

    if( col == 3 ):
        plt.subplot(1, col, 3)
        for size in sizes:
            file_entropy(file=masked_file, window_size=size)
        plt.legend()
        plt.title("Masked Entropy")

    plt.suptitle("Plots showing window sizes")



    files = [benign_file, encrypted_file, masked_file]
    files = [i for i in files if i != ""]
    files = sorted(files, key=lambda x: os.path.getsize(x), reverse=True)
    plt.figure(figsize=(plt_size[0]*len(sizes), plt_size[1]))
    for i, size in enumerate(sizes):
        plt.subplot(1, len(sizes), i+1)
        for j in files:
            file_entropy(file=j, window_size=size, label=j)
        """file_entropy(file=benign_file, window_size=size, label="Unencrypted")
        if(not encrypted_file==""):
            file_entropy(file=encrypted_file, window_size=size, label="Encrypted")
        if(not masked_file==""):
            file_entropy(file=masked_file, window_size=size, label="Masked")"""
        plt.legend()
        plt.title(f"window size = {size}")
    plt.suptitle("Plots Comparing encrypted vs unencrypted window size")

def file_visualize(file: str, file_name: str = "", ax: plt.Axes = None)->None:
    with open(file=file, mode='rb') as f:
        fbytes=f.read()
    if(ax==None):
        _, ax = plt.subplots(1, 1, figsize=(min(100, max(len(fbytes)*6/10000, 15)), 6))
    ax.scatter([i for i in range(len(fbytes))], list(fbytes), marker='.')
    file_name = file if file_name=="" else file_name
    ax.set_title(file_name)
    ax.set_ylabel("Byte values")
    ax.set_xlabel("Byte position")
def nib_mask(encrypted_file: str, probs: Dict[int, Tuple[Tuple[int, ...], Tuple[float, ...]]], ext: str = ".nibmask") -> str:
    nib0: int = 240
    nib1: int = 15
    with open(file=encrypted_file, mode='rb') as f:
        efbytes = f.read()
    split = chain(*map(lambda byte: ( (byte&nib0)>>4, byte&nib1 ), efbytes))
    masked = map(
        lambda nibble: (random.choices(population=probs[nibble][0],weights=probs[nibble][1],k=1)[0] << 4) | nibble,
        split
    )

    outfile=encrypted_file+ext
    with open(file=outfile, mode='wb') as f:
        f.write(bytes(masked))
    
    return outfile

def nib_unmask(masked_file: str) -> None:
    nib1: int = 15
    with open(file=masked_file, mode='rb') as f:
        mefbytes = f.read()
    unmasked = map(lambda a: ((a[0]&nib1)<<4) | a[1]&nib1, zip(mefbytes[:-1:2], mefbytes[1::2]))
    with open(file=masked_file+".unmasked", mode="wb") as f:
        f.write(bytes(unmasked))

