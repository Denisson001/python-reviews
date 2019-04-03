class key_keeper:
    def __init__(self, key):
        self.key = key
        self.pos = 0

    def get_next_char(self):
        c = self.key[self.pos]
        self.pos = (self.pos + 1) % len(self.key)
        return c


def encode_vigenere_cipher(input_file, output_file, key, lang):
    key = key_keeper(key)
    for line in input_file:
        result = ""
        for c in line:
            if c.lower() in lang.alphabet:
                new_c = lang.transform(c.lower(), key.get_next_char())
                if c.lower() != c:
                    new_c = new_c.upper()
                result += new_c
            else:
                result += c
        output_file.write(result)


def decode_vigenere_cipher(input_file, output_file, key, lang):
    key = key_keeper(key)
    for line in input_file:
        result = ""
        for c in line:
            if c.lower() in lang.alphabet:
                reverse_char = lang.num_to_alpha[-lang.alpha_to_num[key.get_next_char()] % len(lang.alphabet)]
                new_c = lang.transform(c.lower(), reverse_char)
                if c.lower() != c:
                    new_c = new_c.upper()
                result += new_c
            else:
                result += c
        output_file.write(result)
