# Linear congruential generator
class RandomGenerator:
    factor = 2416
    const = 374441
    mod = 1771875

    def __init__(self, seed):
        self.last = seed % self.mod

    def get_next(self):
        self.last = (self.factor * self.last + self.const) % self.mod
        return self.last

    def get_in_range(self, left_border, right_border):
        return left_border + self.get_next() % (right_border - left_border + 1)


def encode_vernam_cipher(input_file, output_file, key, lang):
    generator = RandomGenerator(key)
    for line in input_file:
        result_symbols = []
        for char in line:
            if char.lower() in lang.alphabet:
                key = generator.get_in_range(0, len(lang.alphabet) - 1)
                new_char = lang.transform(char.lower(), lang.num_to_alpha[key])
                if char.lower() != char:
                    new_char = new_char.upper()
                result_symbols.append(new_char)
            else:
                result_symbols.append(char)
        output_file.write("".join(result_symbols))


def decode_vernam_cipher(input_file, output_file, key, lang):
    generator = RandomGenerator(key)
    for line in input_file:
        result_symbols = []
        for char in line:
            if char.lower() in lang.alphabet:
                key = generator.get_in_range(0, len(lang.alphabet) - 1)
                reverse_key = -key % len(lang.alphabet)
                new_char = lang.transform(char.lower(), lang.num_to_alpha[reverse_key])
                if char.lower() != char:
                    new_char = new_char.upper()
                result_symbols.append(new_char)
            else:
                result_symbols.append(char)
        output_file.write("".join(result_symbols))
