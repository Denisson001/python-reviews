# Ревью №1. Шифратор

**Settings**

```bash
process        #set encryptor process
               choices = ["encode", "decode", "train", "hack", hack-vigenere]
--cipher       #set encryption type
               choices = ["caesar", "vigenere", "vernam"] 
--key          #set encryption key - any integer for Caesar or Vernam cipher, non empty lowercase string for Vigenere cipher,
	       #max key length (positive integer) for hack Vigenere cipher process
	       #REQUIRED for encode, decode and hack-vigenere processes
--input-file   #set input file
               default = "stdin"
--output-file  #set output file
               default = "stdout"
--text-file    #set input file to train a language model
--model-file   #set language model file, REQUIRED for train, hack and hack-vigenere processes
--language     #set language 
               choices = ["latin", "cyrillic"]
               default = "latin"
```

**Usage example**

Закодировать книжку шифром Цезаря с ключом `13` и положить в `input.txt`

Раскодировать книжку из `input.txt` и положить в `output.txt` 
```
python3 encryptor.py encode --cipher caesar --key 13 --input-file books/orwell_1984_en.txt --output-file input.txt
python3 encryptor.py decode --cipher caesar --key 13 --input-file input.txt --output-file output.txt
```
Аналогично, но уже с книжкой на русском языке и ключом `17`
```
python3 encryptor.py encode --cipher caesar --key 17 --input-file books/bulgakov_master_and_margarita_ru.txt --output-file input.txt --language cyrillic
python3 encryptor.py decode --cipher caesar --key 17 --input-file input.txt --output-file output.txt  --language cyrillic
```
Закодировать книжку шифром Виженера с ключом `lemon` и положить в `input.txt`

Раскодировать книжку из `input.txt` и положить в `output.txt` 
```
python3 encryptor.py encode --cipher vigenere --key lemon --input-file books/shakespeare_the_tragedy_of_hamlet_en.txt --output-file input.txt
python3 encryptor.py decode --cipher vigenere --key lemon --input-file input.txt --output-fil output.txt
```
Закодировать книжку шифром Цезаря с ключом `19` и положить в `input.txt`

Построить простейшую языковую модель на другой книжке и положить статистику в `model.txt`

На основе статистики из `model.txt` раскодировать книжку из `input.txt` и положить результат в `output.txt`
```
python3 encryptor.py encode --cipher caesar --key 19 --input-file books/orwell_1984_en.txt --output-file input.txt
python3 encryptor.py train --text-file books/shakespeare_the_tragedy_of_hamlet_en.txt --model-file model.txt
python3 encryptor.py hack --input-file input.txt --output-file output.txt --model-file model.txt
```
Аналогично, но уже с книжной на русском языке и ключом `21`
```
python3 encryptor.py encode --cipher caesar --key 21 --input-file books/bulgakov_master_and_margarita_ru.txt --output-fil input.txt --language cyrillic
python3 encryptor.py train --text-file books/dostoevsky_crime_and_punishment_ru.txt --model-file model.txt --language cyrillic
python3 encryptor.py hack --input-file input.txt --output-file output.txt --model-file model.txt --language cyrillic
```
Закодировать книжку шифром Вернама с ключом `1234567890` и положить в `input.txt`

Раскодировать книжку из `input.txt` и положить в `output.txt` 
```
python3 encryptor.py encode --cipher vernam --key 1234567890 --input-file books/orwell_1984_en.txt --output-file input.txt
python3 encryptor.py decode --cipher vernam --key 1234567890 --input-file input.txt --output-file output.txt
```
Закодировать текст шифром Виженера с ключом `pineapple` и положить в `input.txt`

Построить простейшую языковую модель на книжке и положить статистику в `model.txt`

На основе статистики из `model.txt` раскодировать книжку из `input.txt` в предположении, что длина ключа при шифровании была не больше `10`, и положить результат в `output.txt`
```
python3 encryptor.py encode --cipher vigenere --key pineapple --input-file books/random_text_en.txt --output-file input.txt
python3 encryptor.py train --text-file books/orwell_1984_en.txt --model-file model.txt
python3 encryptor.py hack-vigenere --key 10 --input-file input.txt --output-file output.txt --model-file model.txt
```
Запустить шифратор на тестах
```
bash tester.sh
```
