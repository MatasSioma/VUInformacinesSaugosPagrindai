# Stud nr - 2314004
# Vardas - Matas Semėnas

import hashlib
import time
from pathlib import Path
from pagalbines_funkcijos import bytes_to_int, int_to_bytes

FAILAS = Path(__file__).parent / "sertifikatas.txt"

VARDAS = "Matas Semėnas"
# RSA raktas iš 6 laboratorinio darbo
e = 47057
n = 9144129007186574290920902149119218750644613146666833760365390329938625796767755536139433691104071761433984145428624239197971982227000513008653266678820491
d = 6784303632358732350530664018789962901189097876821284125117131831377844793389843633932072303142989810942079970900597999045382685430199265177091649680564649


def sha256(duomenys):
    return hashlib.sha256(duomenys).digest()  # baitai, ne hex string

# s = h^d mod n
def pasirasyti(h, d, n):
    return pow(bytes_to_int(h), d, n)

# s^e mod n == h
def patikrinti(h, s, e, n):
    return pow(s, e, n) == bytes_to_int(h)


if __name__ == "__main__":
    # 1. Sertifikatas: vardas pavardė, n, e
    FAILAS.write_text(f"{VARDAS}\n{n}\n{e}", encoding="utf-8", newline="\n")

    # 2. Sertifikato piršto antspaudas ir jo parašas
    hash1 = sha256(FAILAS.read_bytes())
    s1 = pasirasyti(hash1, d, n)
    print(hash1.hex())
    print(s1)

    # 3. Parašas su laiko žyma: SHA256(SHA256(sertifikatas.txt) || ts16)
    ts = int(time.time())
    hash2 = sha256(hash1 + int_to_bytes(ts))
    s2 = pasirasyti(hash2, d, n)
    print()
    print(hash2.hex())
    print(ts)
    print(s2)

    assert patikrinti(hash1, s1, e, n)
    assert patikrinti(hash2, s2, e, n)
