from fastapi import FastAPI
import gensim
import requests
import shutil
import zipfile
import os
import re
import random

#モデルのURL
url = "https://dl.fbaipublicfiles.com/fasttext/vectors-english/wiki-news-300d-1M.vec.zip"
zip_file_name = "wiki-news-300d-1M.vec.zip"
filename = 'wiki-news-300d-1M.vec'

def download_file(url, file_name):
  """指定されたURLからファイルをダウンロードする関数"""
  with requests.get(url, stream=True) as response:
    with open(file_name, 'wb') as file:
      shutil.copyfileobj(response.raw, file)
  print("Download complete.")

def extract_zip(zip_file, extract_to="."):
  """指定されたZIPファイルを解凍する関数"""
  with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(extract_to)
  print("Extraction complete.")
def download_model(url,zip_file_name):
  # ファイルをダウンロード
  download_file(url, zip_file_name)
  # ダウンロードしたZIPファイルを解凍
  extract_zip(zip_file_name)

  print("Download and extraction complete.")
  os.remove(zip_file_name)


def get_words_list(prev_words_list):
     new_words_list = []
     for words in prev_words_list:
       for _ in range(2):
           new_words = words
           list_words = list(new_words)
           tango = random.sample(list_words, 2)
           new_words.remove(tango[0])
           new_words.remove(tango[1])
           if random.choice([True, False]):
               new_tango = model.most_similar(positive=[tango[0], tango[1]])
           else:
               str1, str2 = tango[0], tango[1]
               new_tango = model.most_similar(positive=[str1], negative=[str2])
           # new_tangoは最も類似した単語のリストを返すため、その最初の要素を追加
           new_words.add(new_tango[0][0])  
           new_words.add(new_tango[1][0])  
           new_words.add(new_tango[2][0])  
           new_words_list.append(new_words)
     return new_words_list

def get_target(words_set):
  # アルファベットのみで構成されていない単語をフィルター
  filtered_words = [word for word in words_set if re.fullmatch(r'[a-zA-Z]+', word)]
  # フィルターされた単語が存在しない場合、Noneを返す
  if not filtered_words:
    return None
  # フィルターされた単語の中からランダムに1つ選ぶ
  return random.choice(filtered_words)

#モデルをダウンロードする
if not os.path.exists(filename):
    download_model(url, zip_file_name)
print("start loading model ...")
model = gensim.models.KeyedVectors.load_word2vec_format(filename, binary=False)
print("end loading model ...")
word_list = list(model.key_to_index.keys())
filtered_word_list = [word for word in word_list if re.fullmatch(r'[a-zA-Z]+', word)]
print("word_list size is: ",len(filtered_word_list))
app = FastAPI()

@app.get("/word_merge/")
async def merge_word(str1: str="", str2: str="", op: str=""):
    print(op)
    if op == "plus":
        return {"status": 200, "str": model.most_similar(positive=[str1,str2])}
    if op == "minus":
        return {"status": 200, "str": model.most_similar(positive=[str1],negative=[str2])}
    if op == "similar":
        return {"status": 200, "str": model.most_similar(positive=[str1])}
    return {"status": 400, "detail": "op not found"}

@app.get("/get_problem/")
async def get_problem():
  random_words = random.sample(filtered_word_list,5)
  words_list = [set(random_words)]
  for i in range(6):
    words_list = get_words_list(words_list)
  target = ""
  for words in words_list:
    new_target = get_target(words)
    if new_target == None:
      continue
    target = new_target
    return {"status": 200,"start": random_words,"target": target}
  return {"status":400,"detail":"failed generate problem"}
