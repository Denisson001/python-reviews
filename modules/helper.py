import argparse

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("process", choices = ["encode", "decode", "train", "hack", "hack-vigenere"])
	parser.add_argument("--cipher", choices = ["caesar", "vigenere", "vernam"])
	parser.add_argument("--key")
	parser.add_argument("--input-file")
	parser.add_argument("--output-file")
	parser.add_argument("--text-file")
	parser.add_argument("--model-file")
	parser.add_argument("--language", choices = ["latin", "cyrillic"], default = "latin")
	return parser.parse_args()

def stop_encryptor(error_message):
	print("ERROR: " + error_message)
	exit()

def check_args_correctness(args):
	if ((args.process == "encode" or args.process == "decode")):
		if (args.input_file is not None and args.output_file == args.input_file):
			stop_encryptor("input file and output file are the same")

		if (args.cipher == "caesar" or args.cipher == "vernam"):
			try:
				args.key = int(args.key)
			except:
				stop_encryptor("key isn't an integer")

		if (args.cipher == "vigenere"):
			if (len(args.key) == 0):
				stop_encryptor("wrong key")
				
			for c in args.key:
				if (c not in lang_keeper(args.language).alphabet):
					stop_encryptor("wrong key")

	if (args.process == "train"):
		if (args.model_file is None):
			stop_encryptor("model file not setted")

		if (args.text_file is not None and args.text_file == args.model_file):
			stop_encryptor("text file and model file are the same")

	if (args.process == "hack" or args.process == "hack-vigenere"):
		if (args.model_file is None):
			stop_encryptor("model file not setted")

		if (args.model_file == args.input_file):
			stop_encryptor("input file and model file are the same")

		if (args.model_file == args.output_file):
			stop_encryptor("output file and model file are the same")

		if (args.output_file is not None and args.input_file == args.output_file):
			stop_encryptor("input file and output file are the same")

	if (args.process == "hack-vigenere"):
		try:
			args.key = int(args.key)
		except:
			stop_encryptor("key isn't an integer")

class lang_keeper:
	def __init__(self, lang):
		self.alpha_to_num = dict()
		self.lang = lang

		if (lang == "latin"):
			for c in range(ord("z") - ord("a") + 1):
				self.alpha_to_num[chr(c + ord("a"))] = c
		elif (lang == "cyrillic"):
			for c in range(ord("е") - ord("а") + 1):
				self.alpha_to_num[chr(c + ord("а"))] = c
			self.alpha_to_num["ё"] = 6
			for c in range(ord("я") - ord("е")):
				self.alpha_to_num[chr(c + 6 + ord("а"))] = c + 7

		self.num_to_alpha = dict(zip(self.alpha_to_num.values(), self.alpha_to_num.keys()))
		self.alphabet = {c[0] for c in self.alpha_to_num}

	def transform(self, c1, c2):
		return self.num_to_alpha[(self.alpha_to_num[c1] + self.alpha_to_num[c2]) % len(self.alphabet)]

def save_input(input_file_name, copied_input_file_name):
	with open(copied_input_file_name, "w") as output_file:
		with open(input_file_name, "r") if input_file_name is not None else sys.stdin as input_file:
			for line in input_file:
				output_file.write(line)

def print_data(char_counter, model_file_name, lang):
	lang = lang_keeper(lang)
	with open(model_file_name, "w") if model_file_name is not None else sys.stdout as output_file:
		for i in range(len(lang.alphabet)):
			output_file.write("\'" + lang.num_to_alpha[i] + "\': " + str(char_counter[i]) + "\n")

def normalize_vector(v):
	s = sum(v)
	for i in range(len(v)):
		v[i] /= s
	return v

def standard_deviation(a, b):
	diff = int(0)
	min_len = min(len(a), len(b))
	for i in range(min_len):
		diff += (a[i] - b[i]) ** 2
	return diff / min_len