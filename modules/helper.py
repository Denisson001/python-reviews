import sys
import argparse
from contextlib import contextmanager
import os


def parse_args():
    parser = argparse.ArgumentParser(description="You can encode/decode/hack caesar/vigenere/vernam cipher or train a simple language model")
    subparsers = parser.add_subparsers()

    parser.set_defaults(mode=None)

    encode_subparser = subparsers.add_parser("encode", formatter_class=argparse.ArgumentDefaultsHelpFormatter, help="encode text")
    encode_subparser.set_defaults(mode="encode")
    encode_subparser.add_argument("--cipher", choices=["caesar", "vigenere", "vernam"], required=True, help="Set cipher type")
    encode_subparser.add_argument("--key", required=True, help="Set cipher key")
    encode_subparser.add_argument("--input-file", type=argparse.FileType('r'), default=sys.stdin, help="Set input file")
    encode_subparser.add_argument("--output-file", type=argparse.FileType('w'), default=sys.stdout, help="Set output file")
    encode_subparser.add_argument("--language", choices=["latin", "cyrillic"], default="latin", help="Set language")

    decode_subparser = subparsers.add_parser("decode", formatter_class=argparse.ArgumentDefaultsHelpFormatter, help="decode text")
    decode_subparser.set_defaults(mode="decode")
    decode_subparser.add_argument("--cipher", choices=["caesar", "vigenere", "vernam"], required=True, help="Set cipher type")
    decode_subparser.add_argument("--key", required=True, help="Set cipher key")
    decode_subparser.add_argument("--input-file", type=argparse.FileType('r'), default=sys.stdin, help="Set input file")
    decode_subparser.add_argument("--output-file", type=argparse.FileType('w'), default=sys.stdout, help="Set output file")
    decode_subparser.add_argument("--language", choices=["latin", "cyrillic"], default="latin", help="Set language")

    train_subparser = subparsers.add_parser("train", formatter_class=argparse.ArgumentDefaultsHelpFormatter, help="train a simple language model")
    train_subparser.set_defaults(mode="train")
    train_subparser.add_argument("--text-file", type=argparse.FileType('r'), default=sys.stdin, help="Set text file")
    train_subparser.add_argument("--model-file", type=argparse.FileType('w'), required=True, help="Set model file")
    train_subparser.add_argument("--language", choices=["latin", "cyrillic"], default="latin", help="Set language")

    hack_subparser = subparsers.add_parser("hack", formatter_class=argparse.ArgumentDefaultsHelpFormatter, help="hack text that was encoded with caesar cipher")
    hack_subparser.set_defaults(mode="hack")
    hack_subparser.add_argument("--input-file", type=argparse.FileType('r'), default=sys.stdin, help="Set input file")
    hack_subparser.add_argument("--output-file", type=argparse.FileType('w'), default=sys.stdout, help="Set output file")
    hack_subparser.add_argument("--model-file", type=argparse.FileType('r'), default=sys.stdin, required=True, help="Set model file")
    hack_subparser.add_argument("--language", choices=["latin", "cyrillic"], default="latin", help="Set language")

    hack_vigenere_subparser = subparsers.add_parser("hack-vigenere", formatter_class=argparse.ArgumentDefaultsHelpFormatter, help="hack text that was encoded with vigenere cipher")
    hack_vigenere_subparser.set_defaults(mode="hack-vigenere")
    hack_vigenere_subparser.add_argument("--input-file", type=argparse.FileType('r'), default=sys.stdin, help="Set input file")
    hack_vigenere_subparser.add_argument("--output-file", type=argparse.FileType('w'), default=sys.stdout, help="Set output file")
    hack_vigenere_subparser.add_argument("--model-file", type=argparse.FileType('r'), default=sys.stdin, required=True, help="Set model file")
    hack_vigenere_subparser.add_argument("--key-max-length", required=True, type=int, help="Set key max length")
    hack_vigenere_subparser.add_argument("--language", choices=["latin", "cyrillic"], default="latin", help="Set language")

    return parser.parse_args()


def stop_encryptor(error_message):
    print("ERROR: " + error_message)
    exit()


def check_args_correctness(args):
    args.language = lang_keeper(args.language)

    if args.mode is None:
        stop_encryptor("mode isn`t setted")

    if args.mode == "encode" or args.mode == "decode":
        if args.input_file is not None and args.output_file == args.input_file:
            stop_encryptor("input file and output file are the same")

        if args.cipher == "caesar" or args.cipher == "vernam":
            try:
                args.key = int(args.key)
            except:
                stop_encryptor("key isn't an integer")

        if args.cipher == "vigenere":
            if len(args.key) == 0:
                stop_encryptor("wrong key")

            for c in args.key:
                if c not in args.language.alphabet:
                    stop_encryptor("wrong key")

    if args.mode == "train":
        if args.text_file is not None and args.text_file == args.model_file:
            stop_encryptor("text file and model file are the same")

    if args.mode == "hack" or args.mode == "hack-vigenere":
        if args.model_file == args.input_file:
            stop_encryptor("input file and model file are the same")

        if args.model_file == args.output_file:
            stop_encryptor("output file and model file are the same")

        if args.output_file is not None and args.input_file == args.output_file:
            stop_encryptor("input file and output file are the same")


class lang_keeper:
    def __init__(self, lang):
        self.alpha_to_num = dict()
        self.type = lang

        if lang == "latin":
            for c in range(ord("z") - ord("a") + 1):
                self.alpha_to_num[chr(c + ord("a"))] = c
        elif lang == "cyrillic":
            for c in range(ord("е") - ord("а") + 1):
                self.alpha_to_num[chr(c + ord("а"))] = c
            self.alpha_to_num["ё"] = 6
            for c in range(ord("я") - ord("е")):
                self.alpha_to_num[chr(c + 6 + ord("а"))] = c + 7

        self.num_to_alpha = dict(zip(self.alpha_to_num.values(), self.alpha_to_num.keys()))
        self.alphabet = {c[0] for c in self.alpha_to_num}

    def transform(self, c1, c2):
        return self.num_to_alpha[(self.alpha_to_num[c1] + self.alpha_to_num[c2]) % len(self.alphabet)]


@contextmanager
def remove_file(path):
    try:
        file = open(path, "w")
        file.close()
        yield
    finally:
        os.remove(path)


def save_input(input_file, output_file):
    for line in input_file:
        output_file.write(line)


def standard_deviation(a, b):
    diff = int(0)
    min_len = min(len(a), len(b))
    for i in range(min_len):
        diff += (a[i] - b[i]) ** 2
    return diff / min_len
