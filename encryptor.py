import sys
import modules.caesar as caesar
import modules.vigenere as vigenere
import modules.train as train
import modules.hack as hack
import modules.helper as helper
import modules.vernam as vernam
import modules.hack_vigenere as hack_vigenere

def run():
	args = helper.parse_args()

	helper.check_args_correctness(args)

	if (args.process == "train"):
		char_counter = train.train(args.text_file, args.language)
		helper.print_data(char_counter, args.model_file, args.language)

	elif (args.process == "hack"):
		hack.hack(args.input_file, args.output_file, args.model_file, args.language)

	elif (args.process == "encode" or args.process == "decode"):
		module_name = sys.modules["modules." + args.cipher]
		func_name = args.cipher + "_encryptor";
		getattr(module_name, func_name)(args.input_file, args.output_file, args.process, args.key, args.language)

	elif (args.process == "hack-vigenere"):
		hack_vigenere.hack_vigenere(args.input_file, args.output_file, args.model_file, args.key, args.language)

run()
