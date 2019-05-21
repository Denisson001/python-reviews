import random


BUCKET_SIZE = 4
BYTE_SIZE = BUCKET_SIZE * 2
BYTES_COUNT = 2


def get_xor_value():
    return random.randint(0, (1 << (BYTE_SIZE * BYTES_COUNT)) - 1)


def encode_bucket(bucket):
    if bucket < 10:
        return chr(ord('0') + bucket)
    return chr(ord('A') + bucket)


def decode_bucket(bucket):
    if '0' <= bucket <= '9':
        return ord(bucket) - ord('0')
    return ord(bucket) - ord('A')


def encode_to_bytes(char):
    value = ord(char)
    result = list()
    for bucket_num in range(BYTES_COUNT * BYTE_SIZE // BUCKET_SIZE):
        bucket = value % (1 << BUCKET_SIZE)
        value >>= BUCKET_SIZE
        result.append(encode_bucket(bucket))
    return "".join(reversed(result))


def decode_from_bytes(bytes_bucket):
    result = 0
    for bucket_num in range(BYTES_COUNT * BYTE_SIZE // BUCKET_SIZE):
        result = (result << BUCKET_SIZE) ^ decode_bucket(bytes_bucket[bucket_num])
    return chr(result)


def encode_vernam_cipher(input_file, output_file, key, lang):
    random.seed(key)
    for line in input_file:
        result_symbols = []
        for char in line:
            new_char = chr(ord(char) ^ get_xor_value())
            result_symbols.append(encode_to_bytes(new_char) + ' ')
        output_file.write("".join(result_symbols))


def decode_vernam_cipher(input_file, output_file, key, lang):
    random.seed(key)
    for line in input_file:
        result_symbols = []
        for bytes_tuple in line.split(' ')[:-1]:
            new_char = chr(ord(decode_from_bytes(bytes_tuple)) ^ get_xor_value())
            result_symbols.append(new_char)
        output_file.write("".join(result_symbols))

