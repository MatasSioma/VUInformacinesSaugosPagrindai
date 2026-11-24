# Matas Semėnas
# Stud nr - 2314004
# Variantas - 5

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "AES"))  # aes_helpers iš AES aplanko

from aes import encrypt_block, decrypt_block # Iš 9 lab darbo
from aes_helpers import byte_string_to_blocks, blocks_to_string

FAILAS = Path(__file__).parent / "5.txt"


def xor(a, b):
    return [[a[i][j] ^ b[i][j] for j in range(4)] for i in range(4)]


def ecb(blocks, keys, iv):
    return [decrypt_block(c, keys) for c in blocks]

def cbc(blocks, keys, iv):
    result, prev = [], iv
    for c in blocks:
        result.append(xor(decrypt_block(c, keys), prev))
        prev = c
    return result

def pcbc(blocks, keys, iv):
    result, prev = [], iv
    for c in blocks:
        p = xor(decrypt_block(c, keys), prev)
        result.append(p)
        prev = xor(p, c)
    return result

def cfb(blocks, keys, iv):
    result, prev = [], iv
    for c in blocks:
        result.append(xor(encrypt_block(prev, keys), c))
        prev = c
    return result

def ofb(blocks, keys, iv):
    result, stream = [], iv
    for c in blocks:
        stream = encrypt_block(stream, keys)
        result.append(xor(stream, c))
    return result


def skaityti(failas):
    eilutes = [e.strip() for e in failas.read_text().splitlines() if e.strip()]
    raktas = eilutes[0].split("=")[1].strip()
    iv = eilutes[1].split("=")[1].strip()
    sifrai = [e for e in eilutes[2:] if not e.endswith(".")]
    return raktas, iv, sifrai


if __name__ == "__main__":
    raktas, iv, sifrai = skaityti(FAILAS)
    keys = byte_string_to_blocks(raktas)  # 4 raktai -> 3 raundai
    iv = byte_string_to_blocks(iv)[0]

    rezimai = [("AES-ECB", ecb), ("AES-CBC", cbc), ("AES-PCBC", pcbc), ("AES-CFB", cfb), ("AES-OFB", ofb)]
    for (pavadinimas, f), sifras in zip(rezimai, sifrai):
        print(f"{pavadinimas}: {blocks_to_string(f(byte_string_to_blocks(sifras), keys, iv))}")
