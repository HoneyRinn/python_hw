import sys


def decrypt(cipher_text: str) -> str:
    result = []
    i = 0

    while i < len(cipher_text):
        if cipher_text[i] == ".":
            if i + 1 < len(cipher_text) and cipher_text[i + 1] == ".":
                if result:
                    result.pop()
                i += 2
            else:
                i += 1
        else:
            result.append(cipher_text[i])
            i += 1

    return "".join(result)


if __name__ == "__main__":
    cipher_text = sys.stdin.read().rstrip("\n")
    print(decrypt(cipher_text))