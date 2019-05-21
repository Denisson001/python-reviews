def encode_caesar_cipher(input_file, output_file, key, lang):
    key = lang.num_to_alpha[key % len(lang.alphabet)]

    for line in input_file:
        result_symbols = []
        for char in line:
            if char.lower() in lang.alphabet:
                new_char = lang.transform(char.lower(), key)
                if char.lower() != char:
                    new_char = new_char.upper()
                result_symbols.append(new_char)
            else:
                result_symbols.append(char)
        output_file.write("".join(result_symbols))


def decode_caesar_cipher(input_file, output_file, key, lang):
    return encode_caesar_cipher(input_file, output_file, -key % len(lang.alphabet), lang)
