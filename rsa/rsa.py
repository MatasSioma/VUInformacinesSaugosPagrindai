# Stud nr - 2314004
# Variantas - 5
# Vardas - Matas Semėnas

import math
import secrets
from pagalbines_funkcijos import string_to_int, int_to_string, int_to_bytes

def primeGen(e):
    while True:
        p = 2**255 + secrets.randbelow(2**255)  # atsitiktinis 256 bitų skaičius
        if pow(2, p - 1, p) == 1 and p % e != 1:
            return p

#47057
def keyGen(e):
    p = primeGen(e)
    q = primeGen(e)
    n = p*q
    eulerio = (p-1)*(q-1)
    d = pow(e, -1, eulerio)

    return {
        "p": p,
        "q": q,
        "public":(e, n),
        "private": (d, n)
    }

# dvejetainė paieška
def root(c, e):
    lo, hi = 0, c
    while lo < hi:
        mid = (lo + hi) // 2
        if mid**e < c: lo = mid + 1
        else: hi = mid
    return lo

# mažas n dalikliss
def smallFactor(n):
    x = y = 2
    while True:
        x = (x*x + 1) % n
        y = (y*y + 1) % n
        y = (y*y + 1) % n
        p = math.gcd(x - y, n)
        if p > 1: return p


if __name__ == "__main__":
    # 1.
    e = 47057
    keys = keyGen(e)
    print(keys["p"])
    print(keys["q"])
    print(keys["public"])
    print(keys["private"])

    # 2.
    e, n = keys["public"]
    print(pow(string_to_int("Matas Semėnas"), e, n))

    # 3.
    e, n = 3, 57978193340973369297108562701043535531241438035929130357155046000278533026851
    c = 38173844545078129948288269399042027
    print(int_to_string(root(c, e)))

    # 4.
    e, n = 65537, 99186218111363243410101731962347422165625362610235773539276567172386926970801
    c = 90708548149730452313300412903982774660312730771591279987660619811707542185916
    p = smallFactor(n)
    q = n // p
    d = pow(e, -1, (p-1)*(q-1))
    print(int_to_string(pow(c, d, n)))

    # 5.
    d, n = 52148070181988341913268990845820508970921070792029796935216266921913512716459, 78222105272982512869903486268730763456941215588186365886388080785766717120773
    c = 7798302138285950505767097448918774136832954327394220746974628778518136883860
    m = int_to_bytes(pow(c, d, n))
    print(m[m.index(0) + 1:].decode())
