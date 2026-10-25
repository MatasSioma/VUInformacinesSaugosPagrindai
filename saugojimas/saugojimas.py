# Stud nr - 2314004
# Variantas - 5

import hashlib
import bcrypt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

MD5_HASH = "b3fb79c1d901987585297639cb52522d"
MD5_SALT = "d61eaeba5b1781e7"

SHA256_HASH = "05907ae4fcf755eced760655d7790221b840738cd742186c1840987f90a6c820"
SHA256_SALT = "4e81a60b9599a9d9"

BCRYPT_HASH = "$2b$11$DwhtchaYhmpRQtKSsKoVe.zMAeMEqEuBu5tu7Ul0issmSvMYGeeju"

SCRYPT_HASH = "d466146b10d8f06ca75d0548d51dc3ddef760c02cb201f7ace4622ae4059ba61ff0e949be74ea0d574052fbb58f7b9360a2d42d41d9a0d9e9d932f6bea9eb981"
SCRYPT_SALT = "196ece0e95c71118"
SCRYPT_N = 2 ** 16
SCRYPT_R = 2
SCRYPT_P = 1

ARGON2_HASH = "$argon2id$v=19$m=47104,t=4,p=1$StKuSo6URW7jZyZAJwU0Jg$4K5GCyjmrdWQ6lgJihj+Ka3DM5Z74BlEFfwk0acXCyg"


# "rockyou.txt" > 100MB, todėl suskaidytas į dvi dalis
ROCKYOU_PARTS = ("rockyou_part1.txt", "rockyou_part2.txt")


def words(*paths):
    # "rockyou.txt" - ne UTF-8
    for path in paths:
        with open(path, "rb") as f:
            for line in f:
                yield line.rstrip(b"\r\n")


def crackMD5():
    for pw in words(*ROCKYOU_PARTS):
        if hashlib.md5(pw + MD5_SALT.encode()).hexdigest() == MD5_HASH:
            return pw.decode(errors="replace")
    return None


def crackSHA256():
    for pw in words(*ROCKYOU_PARTS):
        if hashlib.sha256(pw + SHA256_SALT.encode()).hexdigest() == SHA256_HASH:
            return pw.decode(errors="replace")
    return None


def crackBcrypt():
    h = BCRYPT_HASH.encode()
    for pw in words("rockyou_1000.txt"):
        if bcrypt.checkpw(pw, h):
            return pw.decode(errors="replace")
    return None


def crackScrypt():
    salt = SCRYPT_SALT.encode()
    dklen = len(SCRYPT_HASH) // 2
    for pw in words("rockyou_1000.txt"):
        dk = hashlib.scrypt(pw, salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P, dklen=dklen, maxmem=0)
        if dk.hex() == SCRYPT_HASH:
            return pw.decode(errors="replace")
    return None


def crackArgon2():
    ph = PasswordHasher()
    for pw in words("rockyou_1000.txt"):
        try:
            if ph.verify(ARGON2_HASH, pw):
                return pw.decode(errors="replace")
        except VerifyMismatchError:
            continue
    return None


if __name__ == "__main__":
    print("MD5    ", crackMD5())
    print("SHA-256", crackSHA256())
    print("bcrypt ", crackBcrypt())
    print("scrypt ", crackScrypt())
    print("Argon2 ", crackArgon2())
