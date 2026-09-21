"""Decrypt / encrypt Astell&Kern OTA .hex packages (as done by libjniDecHex.so's enc_aes_file).

Scheme (verified against real device output):
  * the file is processed in 16 KiB chunks
  * every FULL chunk is transformed in 16-byte blocks with AES-128-ECB
  * the last partial chunk (size % 16384 bytes) is copied unchanged
  * key = ("%sKOR" % project_name.upper()).ljust(16, "_")   e.g. b"SP3000KOR_______"
  * quirk: the "decrypt" path (mode 0) runs AES *encryption* on the ciphertext, and the
    package is produced with AES *decryption*.  Standard AES-decrypt therefore gives garbage.
"""
import argparse
import os
import sys

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

CHUNK = 0x4000


def make_key(project_name: str) -> bytes:
    return ("%sKOR" % project_name.upper()).ljust(16, "_").encode()


def transform(src: str, dst: str, key: bytes, decrypt_hex: bool) -> None:
    size = os.path.getsize(src)
    if decrypt_hex:
        op = Cipher(algorithms.AES(key), modes.ECB()).encryptor()   # .hex -> zip uses AES *encrypt*
    else:
        op = Cipher(algorithms.AES(key), modes.ECB()).decryptor()   # zip -> .hex uses AES *decrypt*
    done = 0
    with open(src, "rb") as fi, open(dst, "wb") as fo:
        while done < size:
            buf = fi.read(CHUNK)
            if not buf:
                break
            if done + len(buf) < size:          # full, non-final chunk -> transformed
                fo.write(op.update(buf))
            else:                               # final chunk -> copied as-is
                fo.write(buf)
            done += len(buf)
            if (done // CHUNK) % 4096 == 0:
                print(f"\r{done / size * 100:5.1f}%", end="", file=sys.stderr, flush=True)
    print("\rdone      ", file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("mode", choices=["decrypt", "encrypt"])
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--project", default="sp3000", help="ro.boot.project_name of the target model (default sp3000)")
    a = ap.parse_args()
    transform(a.src, a.dst, make_key(a.project), a.mode == "decrypt")
