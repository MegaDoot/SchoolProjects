import random
import os

os.chdir(os.path.dirname(__file__))

def as_bytes(string, encoding="UTF-8", **kwargs):
    return bytearray("hello world", encoding=encoding, **kwargs)

def create_bin(length):
    return bytearray((random.randrange(0, 256) for _ in range(length)))

def write_bin(length, directory=os.getcwd(), name="file.txt"):
    byte_array = create_bin(length)
    print(byte_array)
    with open(name, "wb") as bin_file:
        bin_file.write(b"\x89\x50\x4e\x47\x0d\x0a\x1a\x0a")
        bin_file.write(byte_array)

if __name__ == "__main__":
    write_bin(1000)
    ...
