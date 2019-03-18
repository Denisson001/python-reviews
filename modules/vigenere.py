import sys
import modules.helper as helper


class key_keeper:
    def __init__(self, key):
        self.key = key
        self.pos = 0

    def get_next_char(self):
        c = self.key[self.pos]
        self.pos = (self.pos + 1) % len(self.key)
        return c


def vigenere_encryptor(input_file_name, output_file_name, process, key, lang):
    key = key_keeper(key)
    encryptor = helper.lang_keeper(lang)
    with open(input_file_name, "r") if input_file_name is not None else sys.stdin as input_file:
        with open(output_file_name, "w") if output_file_name is not None else sys.stdout as output_file:
            for line in input_file:
                module_name = sys.modules[__name__]
                func_name = "vigenere_" + process + "r"
                output_file.write(getattr(module_name, func_name)(line, key, encryptor))


def vigenere_encoder(line, key, encryptor):
    result = ""
    for c in line:
        if c.lower() in encryptor.alphabet:
            new_c = encryptor.transform(c.lower(), key.get_next_char())
            if c.lower() != c:
                new_c = new_c.upper()
            result += new_c
        else:
            result += c
    return result


def vigenere_decoder(line, key, encryptor):
    result = ""
    for c in line:
        if c.lower() in encryptor.alphabet:
            reverse_char = encryptor.num_to_alpha[
                -encryptor.alpha_to_num[key.get_next_char()] % len(encryptor.alphabet)]
            new_c = encryptor.transform(c.lower(), reverse_char)
            if c.lower() != c:
                new_c = new_c.upper()
            result += new_c
        else:
            result += c
    return result
