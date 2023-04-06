import fitz
import re
import numpy as np
import pandas as pd
import itertools

pdf_file = 'data/files/unclean/english-kinyarwanda dictionary.pdf'
save_file_ = 'data/files/clean/'
corpus_pattern = "(.*)\s-\s(.*)"
corpus_split_text = "this book will be of some use to those beginning their study of Kinyarwanda."

def open_file(file_path):
  with fitz.open(file_path) as doc:
    text = ''
    for page in doc:
      text += page.get_text()
  return text

def process_english(text):
  text = re.sub(r'\s\([^)]*\)', '', text)
  return (text.split(',')[0],)

def process_kinyarwanda(text):
  text = re.sub(r'\s\([^)]*\)', '', text)
  return tuple(text.split(','))

def combinations(en, rw):
  results = list(
      itertools.product(
          list(en),
          list(rw)
          )
      )
  return results

def extract_dictionary(file_path, save_file='en-rw-dictionary-save.csv'):
  """
  steps:
    1. load file
    2. remove pre corpus data; split at 'ENGLISH-KINYARWANDA'; original 3500 words
    3. collect parallel corpus from dictionary using regex
    4. make combinations for english and kinyarwanda; 4500 combinations
    5. save into a csv file
  """
  dictionary_text = open_file(file_path)
  dictionary_text = dictionary_text.split(corpus_split_text)[1]
  dictionary_corpus_text = re.findall(corpus_pattern, dictionary_text)

  combinated_corpus = []

  for i in range(len(dictionary_corpus_text)):
    item = list(dictionary_corpus_text[i])
    if item[0][0] == '(':
      item[0] = dictionary_corpus_text[i-1][0]
    results = combinations(
        process_english(item[0]),
        process_kinyarwanda(item[1])
    )
    combinated_corpus.extend(results)
  
  df = pd.DataFrame(combinated_corpus, columns=['en', 'rw'])
  df.dropna(inplace=True)
  df.to_csv(save_file_ + save_file, index=False)
  return df

if __name__ == '__main__':
    extract_dictionary(pdf_file)