def train(input_file, lang):
    char_counter = [0] * len(lang.alphabet)

    for line in input_file:
        for c in line:
            if c.lower() in lang.alphabet:
                char_counter[lang.alpha_to_num[c.lower()]] += 1

    return char_counter
