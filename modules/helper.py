import argparse

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


def print_data(char_counter, model_file_name, lang):
	lang = lang_keeper(lang)
	with open(model_file_name, "w") if model_file_name is not None else sys.stdout as output_file:
		for i in range(len(lang.alphabet)):
			output_file.write("\'" + lang.num_to_alpha[i] + "\': " + str(char_counter[i]) + "\n")

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("process", choices = ["encode", "decode", "train", "hack"])
	parser.add_argument("--cipher", choices = ["caesar", "vigenere"])
	parser.add_argument("--key")
	parser.add_argument("--input-file")
	parser.add_argument("--output-file")
	parser.add_argument("--text-file")
	parser.add_argument("--model-file")
	parser.add_argument("--language", choices = ["latin", "cyrillic"], default = "latin")
	return parser.parse_args()

def check_args_correctness(args):
	if (args.process == "train" and args.model_file is None):
		print("model file not setted")
		exit()

	if ((args.process == "encode" or args.process == "decode") and args.cipher == "caesar"):
		try:
			args.key = int(args.key)
		except:
			print("key isn't an integer")
			exit()

	if ((args.process == "encode" or args.process == "decode") and args.cipher == "vigenere"):
		for c in args.key:
			if (c not in lang_keeper(args.language).alphabet):
				print("wrong key")
				exit()
