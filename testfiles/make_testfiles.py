import os

folder = os.path.dirname(__file__)

for name, size in [("small.bin", 5000), ("big.bin", 5000000)]:
    with open(os.path.join(folder, name), "wb") as f:
        f.write(os.urandom(size))
    print("made", name, size, "bytes")