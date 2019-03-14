import sys
import modules.helper as helper

def caesar_encryptor(input_file_name, output_file_name, process, key, lang):
   encryptor = helper.lang_keeper(lang)
   key = int(key) % len(encryptor.alphabet)
   with open(input_file_name, "r") if input_file_name is not None else sys.stdin as input_file:
      with open(output_file_name, "w") if output_file_name is not None else sys.stdout as output_file:
         for line in input_file:
            module_name = sys.modules[__name__]
            func_name = "caesar_" + process + "r";
            output_file.write(getattr(module_name, func_name)(line, key, encryptor))

def caesar_encoder(line, key, encryptor):
   result = ""
   key = encryptor.num_to_alpha[key]
   for c in line:
      if (c.lower() in encryptor.alphabet):
         new_c = encryptor.transform(c.lower(), key)
         if (c.lower() == c):
            new_c = new_c.upper()
         result += new_c 
      else:
         result += c
   return result

def caesar_decoder(line, key, encryptor):
   return caesar_encoder(line, -key % len(encryptor.alphabet), encryptor)
