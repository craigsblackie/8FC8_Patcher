import sys
import re
from pathlib import Path


def convert_hex_string_to_bytes(hex_string: str) -> bytes:
    if len(hex_string) % 2 != 0:
        raise ValueError(f"Invalid hex string length: {hex_string}")
    return bytes.fromhex(hex_string)


def byte_array_to_string(b: bytes) -> str:
    return b.hex().upper()


def signo_at(source: bytes, pattern: bytes):
    for i in range(len(source)):
        if source[i:i + len(pattern)] == pattern:
            yield i
        if i >= 0x1000:
            break


def pattern_at(source: bytes, pattern: str):
    regex = re.compile(pattern)
    pat_len = len(pattern)

    for i in range(len(source)):
        chunk = source[i:i + pat_len]
        if regex.match(byte_array_to_string(chunk)):
            yield i
        if i >= 0x160000:
            break


def main():
    if len(sys.argv) < 2:
        print("Usage: python patcher.py <bios.bin>")
        return -1

    filepath = sys.argv[1]

    try:
        with open(filepath, "rb") as f:
            data = bytearray(f.read())
    except Exception as e:
        print(f"Error reading file: {e}")
        return -1

    filename = Path(filepath).name

    # --- Intel signature check ---
    signo = convert_hex_string_to_bytes("5AA5F00F03")

    found_signature = False
    for index in signo_at(data, signo):
        data[index:index + len(signo)] = signo
        found_signature = True

    if not found_signature:
        print("Error: Intel signature not found")
        return -1

    # --- First pattern ---
    firstpattern = r"^00FCAA([0-9A-Fa-f]{2,4})000000([0-9A-Fa-f]{2,})$"
    replacefirst = convert_hex_string_to_bytes("00FC00")

    first_found = False
    for index in pattern_at(data, firstpattern):
        data[index:index + len(replacefirst)] = replacefirst
        first_found = True

    if first_found:
        try:
            with open(f"patched_{filename}", "wb") as f:
                f.write(data)
        except Exception as e:
            print(f"Error writing file: {e}")
            return -1

    # --- Second pattern ---
    secondpattern = r"^00FDAA([0-9A-Fa-f]{2,4})000000([0-9A-Fa-f]{2,})$"
    replacesecond = convert_hex_string_to_bytes("00FD00")

    second_found = False
    for index in pattern_at(data, secondpattern):
        data[index:index + len(replacesecond)] = replacesecond
        second_found = True

    if second_found:
        try:
            with open(f"patched_{filename}", "wb") as f:
                f.write(data)
        except Exception as e:
            print(f"Error writing file: {e}")
            return -1

        print(f"Patched file saved as patched_{filename}")
        return 0
    else:
        print("No matching patterns found")
        return -1


if __name__ == "__main__":
    sys.exit(main())
