import sys
import modules.helper as helper

def train(input_file_name, lang):
	lang = helper.lang_keeper(lang)
	char_counter = [0] * len(lang.alphabet)

	with open(input_file_name, "r") if input_file_name is not None else sys.stdin as input_file:
		for line in input_file:
			for c in line:		
				if (c.lower() in lang.alphabet):
					char_counter[lang.alpha_to_num[c.lower()]] += 1

	return char_counter
