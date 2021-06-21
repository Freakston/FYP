import struct
from collections import namedtuple
import random
import os

vrDict = {
  "AE": "STRING",
  "AS": "STRING",
  "AT": "ULONG",
  "CS": "STRING",
  "DA": "STRING",
  "DS" : "STRING",
  "DT" : "STRING",
  "FL" : "FLOAT",
  "FD" : "DOUBLE",
  "IS" : "STRING",
  "LO" : "STRING",
  "LT" : "STRING",
  "OB" : "BYTE",
  "OF" : "FLOAT",
  "OW" : "INT",
  "PN" : "STRING",
  "SH" : "STRING",
  "SL" : "LONG",
  "SQ" : "LONG",
  "SS" : "INT",
  "ST" : "STRING",
  "TM" : "STRING",
  "UI" : "STRING",
  "UL" : "LONG",
  "UN" : "BYTE",
  "US" : "INT",
  "UT" : "STRING",
}

def parse_tags(off,data):
    idx = 132
    while idx < len(data):
        print(struct.unpack('<HH',data[idx:idx+4]))
        idx = idx + 4
        print("VR: ",data[idx:idx+2])
        idx = idx + 2
        leng = struct.unpack('<H',data[idx:idx+2])[0]
        print("Len: ",leng)
        idx = idx + 2
        idx = idx + leng
        print(hex(idx))
    return

def findTag(data):
    idx = 0
    while(True):
        if ((8,5) == struct.unpack('<HH',data[idx:idx+4])):
            break
        idx+=1
    
    return idx

def bitFlip(off,data):
    mask = int(random.random()) % 256
    data = bytearray(data)
    randIdx = random.randint(off,len(data) - off - 32)
    for i in range(8):
        data[off + randIdx + i] = data[off + randIdx + i] ^ mask
    
    return bytes(data)

def remBytes(off,data):
    # lets remove a maximux of 8 bytes.
    sliceIdx = random.randint(0,8)
    data = bytearray(data)
    sliceOffset = random.randint(off,len(data))

    return bytes(data[:sliceOffset] + data[sliceOffset+sliceIdx:])

def addBytes(off,data):
    # lets add a maximux of 8 bytes.
    sliceIdx = random.randint(0,8)
    sliceOffset = random.randint(off,len(data))
    randBytes = bytearray(os.urandom(8))
    data = bytearray(data)
    return bytes(data[:sliceOffset] + randBytes + data[sliceOffset+sliceIdx:])

def mut(data):
    off = findTag(data)
    for i in range(0,10):
        case = int(random.random()) % 3
        if case == 0:
            data = bitFlip(off,data)
        elif case == 1:
            data = addBytes(off,data)
        elif case == 2:
            data = remBytes(off,data)

    return data