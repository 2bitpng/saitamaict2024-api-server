from fastapi import FastAPI
import gensim
import requests
import shutil
import zipfile
import os

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

#モデルをダウンロードする
if not os.path.exists(filename):
    download_model(url, zip_file_name)
print("start loading model ...")
model = gensim.models.KeyedVectors.load_word2vec_format(filename, binary=False)
print("end loading model ...")
app = FastAPI()

@app.get("/word_merge/")
async def merge_word(str1: str="", str2: str="", op: str=""):
    print(op)
    if op == "plus":
        return {"status": 200, "str": model.most_similar(positive=[str1,str2])}
    if op == "minus":
        return {"status": 200, "str": model.most_similar(positive=[str1],negative=[str2])}
    if op == "similar":
        return {"status": 200, "str": model.most_similar(positive=[str1],negative=[str2])}
    return {"status": 400, "detail": "op not found"}

