# Stud nr - 2314004
# Variantas - 5  (2314004 mod 10 + 1 = 5)
from aes_helpers import (
    byte_string_to_blocks, string_to_blocks, blocks_to_string, blocks_to_byte_string,
    sbox, sboxInv, mult_2, mult_3, mult_9, mult_b, mult_d, mult_e,
)

RAKTAS = "38e1d0fa257d1a8800865ff4fc2896dd7725f2da24fd0d66aad66e0f80c08efb2178c8945e290500102c7a69914088d75f6326292b7b11bba9ded80f61afc9b4"
SIFRAS = "9ddba6bfdd242b8b7929976fda7687d3"
PAVARDE = "Semėnas"


def add_round_key(state, key):
    return [[state[i][j] ^ key[i][j] for j in range(4)] for i in range(4)]

def sub_bytes(state):
    return [[sbox[b] for b in row] for row in state]

def inv_sub_bytes(state):
    return [[sboxInv[b] for b in row] for row in state]

def shift_rows(state):
    return [row[i:] + row[:i] for i, row in enumerate(state)]

def inv_shift_rows(state):
    return [row[-i:] + row[:-i] if i else row[:] for i, row in enumerate(state)]

def mix_columns(state):
    r = [[0] * 4 for _ in range(4)]
    for c in range(4):
        a0, a1, a2, a3 = (state[i][c] for i in range(4))
        r[0][c] = mult_2[a0] ^ mult_3[a1] ^ a2 ^ a3
        r[1][c] = a0 ^ mult_2[a1] ^ mult_3[a2] ^ a3
        r[2][c] = a0 ^ a1 ^ mult_2[a2] ^ mult_3[a3]
        r[3][c] = mult_3[a0] ^ a1 ^ a2 ^ mult_2[a3]
    return r

def inv_mix_columns(state):
    r = [[0] * 4 for _ in range(4)]
    for c in range(4):
        a0, a1, a2, a3 = (state[i][c] for i in range(4))
        r[0][c] = mult_e[a0] ^ mult_b[a1] ^ mult_d[a2] ^ mult_9[a3]
        r[1][c] = mult_9[a0] ^ mult_e[a1] ^ mult_b[a2] ^ mult_d[a3]
        r[2][c] = mult_d[a0] ^ mult_9[a1] ^ mult_e[a2] ^ mult_b[a3]
        r[3][c] = mult_b[a0] ^ mult_d[a1] ^ mult_9[a2] ^ mult_e[a3]
    return r


# raktai: N + 1 blokų, N - raundų skaičius
def encrypt_block(block, keys):
    N = len(keys) - 1
    state = add_round_key(block, keys[0])
    for n in range(1, N):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, keys[n])
    state = sub_bytes(state)
    state = shift_rows(state)
    return add_round_key(state, keys[N])

def decrypt_block(block, keys):
    N = len(keys) - 1
    state = add_round_key(block, keys[N])
    for n in range(1, N):
        state = inv_shift_rows(state)
        state = inv_sub_bytes(state)
        state = add_round_key(state, keys[N - n])
        state = inv_mix_columns(state)
    state = inv_shift_rows(state)
    state = inv_sub_bytes(state)
    return add_round_key(state, keys[0])


def encrypt(text, keys):
    return blocks_to_byte_string([encrypt_block(b, keys) for b in string_to_blocks(text)])

def decrypt(cipher, keys):
    return blocks_to_string([decrypt_block(b, keys) for b in byte_string_to_blocks(cipher)])


if __name__ == "__main__":
    keys = byte_string_to_blocks(RAKTAS)

    # 1. Atšifravimas
    print("Atšifruotas tekstas:", decrypt(SIFRAS, keys))

    # 2. Pavardės šifravimas
    c = encrypt("Semėnas", keys)
    print("Šifras:", c)
    print("Patikra:", decrypt(c, keys))

    print("Naudotas raktas:", RAKTAS)
