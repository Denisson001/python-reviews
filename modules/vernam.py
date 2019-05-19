import random


def encode_vernam_cipher(input_file, output_file, key, lang):
    random.seed(key)
    for line in input_file:
        result_symbols = []
        for char in line:
            if char.lower() in lang.alphabet:
                key = random.randint(0, len(lang.alphabet) - 1)
                new_char = lang.transform(char.lower(), lang.num_to_alpha[key])
                if char.lower() != char:
                    new_char = new_char.upper()
                result_symbols.append(new_char)
            else:
                result_symbols.append(char)
        output_file.write("".join(result_symbols))


def decode_vernam_cipher(input_file, output_file, key, lang):
    random.seed(key)
    for line in input_file:
        result_symbols = []
        for char in line:
            if char.lower() in lang.alphabet:
                key = random.randint(0, len(lang.alphabet) - 1)
                reverse_key = -key % len(lang.alphabet)
                new_char = lang.transform(char.lower(), lang.num_to_alpha[reverse_key])
                if char.lower() != char:
                    new_char = new_char.upper()
                result_symbols.append(new_char)
            else:
                result_symbols.append(char)
        output_file.write("".join(result_symbols))
