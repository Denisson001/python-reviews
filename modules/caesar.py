def encode_caesar_cipher(input_file, output_file, key, lang):
    key = lang.num_to_alpha[key % len(lang.alphabet)]

    for line in input_file:
        result = ""
        for c in line:
            if c.lower() in lang.alphabet:
                new_c = lang.transform(c.lower(), key)
                if c.lower() != c:
                    new_c = new_c.upper()
                result += new_c
            else:
                result += c
        output_file.write(result)


def decode_caesar_cipher(input_file, output_file, key, lang):
    return encode_caesar_cipher(input_file, output_file, -key % len(lang.alphabet), lang)
