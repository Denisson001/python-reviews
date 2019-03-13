import sys
import modules.helper as helper
import random

#Linear congruential generator
class random_generator:
	def __init__(self, seed):
		self.factor = 2416
		self.const = 374441
		self.mod = 1771875
		self.last = seed % self.mod;

	def get_next(self):
		self.last = (self.factor * self.last + self.const) % self.mod
		return self.last

	def get_in_range(self, l, r):
		return l + self.get_next() % (r - l + 1)

def vernam_encryptor(input_file_name, output_file_name, process, key, lang):
	encryptor = helper.lang_keeper(lang)
	generator = random_generator(key)
	with open(input_file_name, "r") if input_file_name is not None else sys.stdin as input_file:
		with open(output_file_name, "w") if output_file_name is not None else sys.stdout as output_file:
			for line in input_file:
				module_name = sys.modules[__name__]
				func_name = "vernam_" + process + "r";
				output_file.write(getattr(module_name, func_name)(line, generator, encryptor))

def vernam_encoder(line, generator, encryptor):
	result = ""
	for c in line:
		if (c.lower() in encryptor.alphabet):
			key = generator.get_in_range(0, len(encryptor.alphabet) - 1)
			new_c = encryptor.transform(c.lower(), encryptor.num_to_alpha[key])
			if (c.lower() == c):
				new_c = new_c.upper()
			result += new_c 
		else:
			result += c
	return result

def vernam_decoder(line, generator, encryptor):
	result = ""
	for c in line:
		if (c.lower() in encryptor.alphabet):
			key = generator.get_in_range(0, len(encryptor.alphabet) - 1)
			reverse_key = -key % len(encryptor.alphabet)
			new_c = encryptor.transform(c.lower(), encryptor.num_to_alpha[reverse_key])
			if (c.lower() == c):
				new_c = new_c.upper()
			result += new_c 
		else:
			result += c
	return result
