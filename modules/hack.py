import modules.caesar as caesar
import modules.train as train
import modules.helper as helper


def read_data(model_file, lang):
    char_counter = [0] * len(lang.alphabet)

    for i in range(len(lang.alphabet)):
        char_counter[i] = int(model_file.readline().replace("\n", "").split(" ")[1])

    return char_counter


def normalize_vector(v):
    s = sum(v)
    for i in range(len(v)):
        v[i] /= s


def hack(input_file, output_file, model_file, lang, only_return_key=False):
    char_counter = read_data(model_file, lang)
    normalize_vector(char_counter)

    best_key, min_diff = -1, 0
    fake_input_file_name = "temp/hack_temp_file_1.txt"
    fake_output_file_name = "temp/hack_temp_file_2.txt"

    with helper.remove_file(fake_input_file_name), helper.remove_file(fake_output_file_name):
        with open(fake_input_file_name, "w") as fake_input_file:
            helper.save_input(input_file, fake_input_file)

        for key in range(len(lang.alphabet)):
            with open(fake_input_file_name, "r") as fake_input_file, open(fake_output_file_name, "w") as fake_output_file:
                caesar.decode_caesar_cipher(fake_input_file, fake_output_file, key, lang)

            with open(fake_output_file_name, "r") as fake_output_file:
                new_char_counter = train.train(fake_output_file, lang)

            normalize_vector(new_char_counter)

            diff = helper.standard_deviation(char_counter, new_char_counter)
            if best_key == -1 or min_diff > diff:
                best_key, min_diff = key, diff

        if only_return_key:
            return best_key

        with open(fake_input_file_name, "r") as fake_input_file:
            caesar.decode_caesar_cipher(fake_input_file, output_file, best_key, lang)
