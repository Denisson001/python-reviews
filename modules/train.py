def train(input_file, lang):
    char_counter = [0] * len(lang.alphabet)

    for line in input_file:
        for char in line:
            if char.lower() in lang.alphabet:
                char_counter[lang.alpha_to_num[char.lower()]] += 1

    return char_counter
