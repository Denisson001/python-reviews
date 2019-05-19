import sys
import os
import modules.caesar as caesar
import modules.vigenere as vigenere
import modules.train as train
import modules.hack as hack
import modules.helper as helper
import modules.vernam as vernam
import modules.hack_vigenere as hack_vigenere


def print_data(char_counter, model_file, lang):
    for i in range(len(lang.alphabet)):
        model_file.write("\'" + lang.num_to_alpha[i] + "\': " + str(char_counter[i]) + "\n")


def run():
    args = helper.parse_args()

    helper.check_args_correctness(args)

    if args.mode == "train":
        char_counter = train.train(args.text_file, args.language)
        print_data(char_counter, args.model_file, args.language)

    elif args.mode == "hack":
        hack.hack(args.input_file, args.output_file, args.model_file, args.language)

    elif args.mode == "encode" or args.mode == "decode":
        module_name = sys.modules["modules." + args.cipher]
        func_name = args.mode + "_" + args.cipher + "_cipher"
        getattr(module_name, func_name)(args.input_file, args.output_file, args.key, args.language)

    elif args.mode == "hack-vigenere":
        hack_vigenere.hack_vigenere(args.input_file, args.output_file, args.model_file, args.key_max_length, args.language)


if __name__ == "__main__":
    if not os.path.exists("temp"):
        os.makedirs("temp")
    
    run()
