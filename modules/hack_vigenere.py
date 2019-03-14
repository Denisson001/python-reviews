import modules.helper as helper
import modules.train as train
import modules.hack as hack

def calc_index_vector(input_file_name, period_len, lang):
   lang = helper.lang_keeper(lang)
   char_counter = [[0] * len(lang.alphabet) for i in range(period_len)]
   pos = int(0)
   
   with open(input_file_name, "r") as input_file:
      for line in input_file:
         for c in line:
            if (c.lower() in lang.alphabet):
               char_counter[pos][lang.alpha_to_num[c.lower()]] += 1
               pos = (pos + 1) % period_len

   index_vector = [0] * period_len
   for i in range(period_len):
      sum_count = int(0)
      for c in range(len(lang.alphabet)):
         sum_count += char_counter[i][c]
         index_vector[i] += char_counter[i][c] * (char_counter[i][c] - 1)
      index_vector[i] /= sum_count * (sum_count - 1)

   return index_vector

def calc_key_len(input_file_name, max_key_len, lang):
   lang_index = 0
   if (lang == "latin"):
      lang_index = 0.0644
   else:
      lang_index = 0.0553
   best_key_len, min_diff = -1, 0

   for key_len in range(1, max_key_len):
      index_vector = calc_index_vector(input_file_name, key_len, lang)
      model_index_vector = [lang_index] * key_len
      diff = helper.standard_deviation(index_vector, model_index_vector)
      if (best_key_len == -1 or min_diff > diff):
         best_key_len, min_diff = key_len, diff

   return best_key_len

def calc_keys(input_file_name, model_file_name, key_len, lang):
   keys = [0] * key_len
   tmp_file_name = "tmp/tmp4.txt"
   tmp2_file_name = "tmp/tmp5.txt"

   for remainder in range(key_len):
      pos = int(0)
      with open(tmp_file_name, "w") as output_file:
         with open(input_file_name, "r") as input_file:
            for line in input_file:
               for c in line:
                  if (c.lower() in helper.lang_keeper(lang).alphabet):
                     if (pos == remainder):
                        output_file.write(c.lower())
                     pos = (pos + 1) % key_len
      keys[remainder] = hack.hack(tmp_file_name, tmp2_file_name, model_file_name, lang)

   return keys

def hack_vigenere(input_file_name, output_file_name, model_file_name, max_key_len, lang):
   copied_input_file_name = "tmp/tmp3.txt"
   helper.save_input(input_file_name, copied_input_file_name)
   input_file_name = copied_input_file_name

   key_len = calc_key_len(input_file_name, max_key_len, lang)
   keys = calc_keys(input_file_name, model_file_name, key_len, lang)
   lang = helper.lang_keeper(lang)

   with open(input_file_name, "r") as input_file:
      with open(output_file_name, "w") as output_file:
         pos = int(0)
         for line in input_file:
            for c in line:
               if (c.lower() in lang.alphabet):
                  reverse_char = lang.num_to_alpha[-keys[pos] % len(lang.alphabet)]
                  new_c = lang.transform(c.lower(), reverse_char)
                  if (c.lower() == c):
                     new_c = new_c.upper()
                  output_file.write(new_c)
                  pos = (pos + 1) % key_len
               else:
                  output_file.write(c)