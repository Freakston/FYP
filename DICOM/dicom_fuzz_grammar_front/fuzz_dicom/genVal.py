import random

# Magic numbers borrowed from Gynveal's fuzzing streams
MAGIC_8 = [0, 2, 0x7f, 0xff, 64, 32]
MAGIC_16 = MAGIC_8 + [0xffff, 0x7fff, 0x3fff, 0xfff, 0x100]
MAGIC_32 = MAGIC_16 + [0xffffffff, 0x80000000, 0x40000000, 0x7fffffff]
MAGIC_64 = MAGIC_32 + [0xffffffffffffffff, 0x8000000000000000, 0x4000000000000000, 0x7fffffffffffffff]
MAGIC_128 = MAGIC_64 + [0xffffffffffffffffffffffffffffffff, 0x80000000000000000000000000000000, 0x40000000000000000000000000000000,
        0x7fffffffffffffffffffffffffffffff]
MAGIC_256 = MAGIC_128 + [0xffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, 0x8000000000000000000000000000000000000000000000000000000000000000,
        0x4000000000000000000000000000000000000000000000000000000000000000, 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]

SIGNED_MAGIC_8 = [0, 2, 0x7f, 1, 64, 32, -0, -2, -0x7f, -1, -64, -32]
SIGNED_MAGIC_16 = SIGNED_MAGIC_8 + [0x4fff, 0x7fff, 0x3fff, 0xfff, 0x100, -0x4fff, -0x7fff, -0x3fff, -0xfff, -0x100]
SIGNED_MAGIC_32 = SIGNED_MAGIC_16 + [0x1fffffff, 0x80000000, 0x40000000, 0x7fffffff, -0x1fffffff, -0x80000000, -0x40000000, -0x7fffffff]
SIGNED_MAGIC_64 = SIGNED_MAGIC_32 + [0x1fffffffffffffff, 0x8000000000000000, 0x4000000000000000, 0x7fffffffffffffff, -0x1fffffffffffffff, -0x8000000000000000, -0x4000000000000000, -0x7fffffffffffffff]
SIGNED_MAGIC_128 = SIGNED_MAGIC_64 + [0x1fffffffffffffffffffffffffffffff, 0x80000000000000000000000000000000, 0x40000000000000000000000000000000,
        0x7fffffffffffffffffffffffffffffff, -0x1fffffffffffffffffffffffffffffff, -0x80000000000000000000000000000000, -0x40000000000000000000000000000000,
        -0x7fffffffffffffffffffffffffffffff]
SIGNED_MAGIC_256 = SIGNED_MAGIC_128 + [0x1fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, 0x8000000000000000000000000000000000000000000000000000000000000000,
        0x4000000000000000000000000000000000000000000000000000000000000000, 0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, 
        -0x1fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff, -0x8000000000000000000000000000000000000000000000000000000000000000,
        -0x4000000000000000000000000000000000000000000000000000000000000000, -0x7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff]

def get_number_of_width(width, signed):
    if random.randint(0, 10) == 1:
        if signed:
            limit = (2 ** (width - 1)) - 1
            return str(random.randint(- limit, limit))
        else:
            return str(random.randint(0, (2 ** width) - 1))
    if width == 8:
        if signed:
            return str(random.choice(SIGNED_MAGIC_8))
        else:
            return str(random.choice(MAGIC_8))
    elif width == 16:
        if signed:
            return str(random.choice(SIGNED_MAGIC_16))
        else:
            return str(random.choice(MAGIC_16))
    elif width == 32:
        if signed:
            return str(random.choice(SIGNED_MAGIC_32))
        else:
            return str(random.choice(MAGIC_32))
    elif width == 64:
        if signed:
            return str(random.choice(SIGNED_MAGIC_64))
        else:
            return str(random.choice(MAGIC_64))
    elif width == 128:
        if signed:
            return str(random.choice(SIGNED_MAGIC_128))
        else:
            return str(random.choice(MAGIC_128))
    else:
        if signed:
            return str(random.choice(SIGNED_MAGIC_256))
        else:
            return str(random.choice(MAGIC_256))