# Stud nr - 2314004
# Variantas - 5 

# Šifruoti: Lenk medį, kol jaunas. 11
# DeŠifruoti: Suęų hųęk vęocm ųšęif. ?

ABC = "aąbcčdeęėfghiįyjklmnoprsštuųūvzž"
BASE = [f'{a}' for a in ABC]

def cezarEncrypt(s, n):
    res = ""
    for x in s:
        try:
            y = BASE[(BASE.index(x.lower()) + n) % len(BASE)]
            if x.islower(): res += y
            else: res += y.upper()
        except ValueError: # Abecelej raidės nėra
            res += x

    return res

def cezarDecrypt(s):
    for n in range(len(BASE)):
        print(f"{n}: {cezarEncrypt(s, n)}")


if __name__ == "__main__":
    print(cezarEncrypt("Lenk medį, kol jaunas.", 11))
    # Ats.: "Ūlzų vlkš, ųžū uhdzhb"

    cezarDecrypt("Suęų hųęk vęocm ųšęif.")
    # Ats.: "Ūžia kaip bitės avily" 
    # (cezarEncrypt("Ūžia kaip bitės avily.", 27) -> "Suęų hųęk vęocm ųšęif.")