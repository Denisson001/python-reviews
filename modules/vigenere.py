class KeyKeeper:
    def __init__(self, key):
        self.key = key
        self.pos = 0

    def get_next_char(self):
        next_char = self.key[self.pos]
        self.pos = (self.pos + 1) % len(self.key)
        return next_char


def encode_vigenere_cipher(input_file, output_file, key, lang):
    key = KeyKeeper(key)
    for line in input_file:
        result_symbols = []
        for char in line:
            if char.lower() in lang.alphabet:
                new_char = lang.transform(char.lower(), key.get_next_char())
                if char.lower() != char:
                    new_char = new_char.upper()
                result_symbols.append(new_char)
            else:
                result_symbols.append(char)
        output_file.write("".join(result_symbols))


def decode_vigenere_cipher(input_file, output_file, key, lang):
    key = KeyKeeper(key)
    for line in input_file:
        result_symbols = []
        for char in line:
            if char.lower() in lang.alphabet:
                reversed_char = lang.num_to_alpha[-lang.alpha_to_num[key.get_next_char()] % len(lang.alphabet)]
                new_char = lang.transform(char.lower(), reversed_char)
                if char.lower() != char:
                    new_char = new_char.upper()
                result_symbols.append(new_char)
            else:
                result_symbols.append(char)
        output_file.write("".join(result_symbols))
