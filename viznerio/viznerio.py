# Stud nr - 2314004
# Variantas - 5 

# 1.
# Atšifruoti: Mrėszjčs ęįškhrėaf ėy gšįzžzjzs sryif lyabūfa.
# Raktas: mūša

from collections import defaultdict

ABC = "aąbcčdeęėfghiįyjklmnoprsštuųūvzž"
BASE = [f'{a}' for a in ABC]

def decrypt(S, R):
    Ri = [BASE.index(r.lower()) for r in R]
    A = ""
    ri = 0

    for s in S:
        try:
            a = BASE[(BASE.index(s.lower()) - Ri[ri]) % len(BASE)]
            ri += 1
            if s.islower(): A += a
            else: A += a.upper()
            if len(Ri) == ri: ri = 0
        except ValueError: # Abecelej raidės nėra
            A += s

    return A

def findKeyLen(S):
    T = [s.lower() for s in S if s.lower() in ABC]

    digmap = {}
    for i in range(len(T) - 1):
        dig = T[i] + T[i + 1]
        for k in range(i + 1, len(T) - 1):
            if dig == T[k] + T[k + 1]:
                digmap[(i, k)] = k - i

    # Daliklių dažnių lentelė
    divmap = defaultdict(int)
    for d in digmap.values():
        for n in range(2, 20 + 1):
            if d % n == 0:
                divmap[n] += 1

    print("Daliklis | Dažnis")
    for n in range(2, 20 + 1):
        print(f"{n:8} | {divmap[n]}")

    return divmap


def findKey(S, L):
    T = "".join(s.lower() for s in S if s.lower() in ABC)

    Svar = {}
    for l in range(L):
        Sl = T[l::L] # Kas L-asis simbolis pradedant nuo l-ojo
        for a in ABC:
            Svar[(l, a)] = decrypt(Sl, a)

    def freqTest(A):
        return sum(A.count(c) for c in "iasore") / len(A)
    
    R = ""
    for l in range(L):
        # Teisingas poslinkis tas, kuriame dažniausių raidžių I A S O R E yra apie 50%
        a, f = max(((a, freqTest(Svar[(l, a)])) for a in ABC), key=lambda x: x[1])
        # print(f"S{l + 1}: poslinkis {a}, f = {f:.2f}")
        R += a

    print(f"\nRaktas: {R}")
    return R


if __name__ == "__main__":
    print(decrypt("Mrėszjčs ęįškhrėaf ėy gšįzžzjzs sryif lyabūfa.", "mūša"))
    # Ats.: Auksinis plaktukas ir geležines duris prakala.
    
    with open("5.txt", "r") as file:
        S = file.read()

    # findKeyLen(S) # Pikai ties 7 ir 14
    R = findKey(S, 14)
    # Ats.: viešasisraktas
    print()
    print(decrypt(S, R))