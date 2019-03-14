import sys
import modules.caesar as caesar
import modules.train as train
import modules.helper as helper

def read_data(model_file_name, lang):
   lang = helper.lang_keeper(lang)
   char_counter = [0] * len(lang.alphabet)

   with open(model_file_name, "r") as model_file:
      for i in range(len(lang.alphabet)):
         char_counter[i] = int(model_file.readline().replace("\n", "").split(" ")[1])

   return char_counter

def hack(input_file_name, output_file_name, model_file_name, lang):
   char_counter = read_data(model_file_name, lang)
   helper.normalize_vector(char_counter)

   best_key, min_diff = -1, 0
   tmp_file_name = "tmp/tmp.txt"
   copied_input_file_name = "tmp/tmp2.txt"
   
   helper.save_input(input_file_name, copied_input_file_name)
   input_file_name = copied_input_file_name

   for key in range(len(helper.lang_keeper(lang).alphabet)):
      caesar.caesar_encryptor(input_file_name, tmp_file_name, "decode", key, lang)
      new_char_counter = train.train(tmp_file_name, lang)
      helper.normalize_vector(new_char_counter)

      diff = helper.standard_deviation(char_counter, new_char_counter)
      if (best_key == -1 or min_diff > diff):
         best_key, min_diff = key, diff

   caesar.caesar_encryptor(input_file_name, output_file_name, "decode", best_key, lang)

   return best_key