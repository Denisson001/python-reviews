# Linear congruential generator
class random_generator:
    factor = 2416
    const = 374441
    mod = 1771875

    def __init__(self, seed):
        self.last = seed % self.mod

    def get_next(self):
        self.last = (self.factor * self.last + self.const) % self.mod
        return self.last

    def get_in_range(self, l, r):
        return l + self.get_next() % (r - l + 1)


def encode_vernam_cipher(input_file, output_file, key, lang):
    generator = random_generator(key)
    for line in input_file:
        result = ""
        for c in line:
            if c.lower() in lang.alphabet:
                key = generator.get_in_range(0, len(lang.alphabet) - 1)
                new_c = lang.transform(c.lower(), lang.num_to_alpha[key])
                if c.lower() != c:
                    new_c = new_c.upper()
                result += new_c
            else:
                result += c
        output_file.write(result)


def decode_vernam_cipher(input_file, output_file, key, lang):
    generator = random_generator(key)
    for line in input_file:
        result = ""
        for c in line:
            if c.lower() in lang.alphabet:
                key = generator.get_in_range(0, len(lang.alphabet) - 1)
                reverse_key = -key % len(lang.alphabet)
                new_c = lang.transform(c.lower(), lang.num_to_alpha[reverse_key])
                if c.lower() != c:
                    new_c = new_c.upper()
                result += new_c
            else:
                result += c
        output_file.write(result)
