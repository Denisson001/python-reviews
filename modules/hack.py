import sys
import modules.caesar as caesar
import modules.train as train
import modules.helper as helper

def read_data(model_file_name, lang):
	lang = helper.lang_keeper(lang)
	char_counter = [0]*len(lang.alphabet)

	with open(model_file_name, "r") as model_file:
		for i in range(len(lang.alphabet)):
			char_counter[i] = int(model_file.readline().replace("\n", "").split(" ")[1])

	return char_counter

def calc_diff(char_counter, new_char_counter):
	diff = int(0)
	sum1 = sum(char_counter)
	sum2 = sum(new_char_counter)

	for i in range(len(char_counter)):
		diff += (100 * char_counter[i] / sum1 - 100 * new_char_counter[i] / sum2)**2
	return diff

def hack(input_file_name, output_file_name, model_file_name, lang):
	char_counter = read_data(model_file_name, lang)

	best_key, min_diff = -1, 0
	tmp_file_name = "tmp/tmp.txt"
	copied_input_file_name = "tmp/tmp2.txt"

	with open(copied_input_file_name, "w") as output_file:
		with open(input_file_name, "r") if input_file_name is not None else sys.stdin as input_file:
			for line in input_file:
				output_file.write(line)

	input_file_name = copied_input_file_name

	for key in range(len(helper.lang_keeper(lang).alphabet)):
		caesar.caesar_encryptor(input_file_name, tmp_file_name, "decode", key, lang)
		new_char_counter = train.train(tmp_file_name, lang)
		diff = calc_diff(char_counter, new_char_counter)
		if (best_key == -1 or min_diff > diff):
			best_key, min_diff = key, diff

	caesar.caesar_encryptor(input_file_name, output_file_name, "decode", best_key, lang)