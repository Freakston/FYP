import random

def blockMutate(buf,times):
    blockStart = random.randint(0,len(buf))
    blockLen = random.randint(0,0x20)
    for i in range(blockLen):
        buf[blockStart + i] = random.randint(0x00,0xff)

def byteMutate(data,n):
    buf = list(data)
    chance = random.randint(0,9)
    for i in range(n):
        buf[random.randint(0,len(buf)-1)] = chr(random.randint(0x01,0xff))

    if chance == 1:
        buf.append(chr(random.randint(0x01, 0xff)))
    return "".join([i for i in buf])
