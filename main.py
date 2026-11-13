#!/usr/bin/env python3
"""news-image-01 entry program: reproduce entry.png.

Reads the entry image bundled in this repository and writes an identical
copy to /output/entry.png, streaming in chunks and verifying the copy's
SHA-256 against the source before exiting.
"""
import hashlib
import os

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
DST = "/output/entry.png"
CHUNK = 1024 * 1024


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(CHUNK), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(SRC, "rb") as src, open(DST, "wb") as dst:
        while True:
            chunk = src.read(CHUNK)
            if not chunk:
                break
            dst.write(chunk)
    src_hash = sha256_of(SRC)
    dst_hash = sha256_of(DST)
    if src_hash != dst_hash:
        raise SystemExit(f"checksum mismatch: {src_hash} != {dst_hash}")
    print(f"wrote {DST} ({os.path.getsize(DST)} bytes, sha256 {dst_hash})")


if __name__ == "__main__":
    main()
