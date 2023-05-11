"""
This is an implementation of word level substitution
by using synonyms for both english and kinyarwanda
"""

import pandas as pd
import numpy as np
import re
import itertools
import random
import nltk


data_file = 'data/files/clean/data.csv'
dictionary_file = 'data/files/clean/en-rw-dictionary.csv'
save_file = 'data/files/clean/data-substituted.csv'
columns = ['en','rw']
en_train_data = 'data/train/train-en.txt'
rw_train_data = 'data/train/train-rw.txt'

with open(en_train_data, 'r', encoding='utf-8') as f:
  en_list = [line.strip() for line in f.readlines()]
  
with open(rw_train_data, 'r', encoding='utf-8') as f:
  rw_list = [line.strip() for line in f.readlines()]

dictionary_df = pd.read_csv(dictionary_file)
dictionary_df.dropna(inplace=True)

# data_df = pd.DataFrame({'en':en_list, 'rw':rw_list})
data_df = pd.read_csv(data_file)

def get_rw_synonyms(word, df=dictionary_df):
  """
  gets synonyms to replace in kinyarwanda column
  """
  synonyms_word_filter = df[df["rw"]==word]
  synonyms = []
  if len(synonyms_word_filter)>0:
    synonyms = list(set(synonyms_word_filter["rw_synonyms"].values[0].split(", ")))
  
  return synonyms

def get_en_synonyms(word, df=dictionary_df):
  """
  get synonyms to replace in english column
  """
  synonyms_word_filter = df[df["en"]==word]
  synonyms = []
  if len(synonyms_word_filter)>0:
    synonyms = list(set(synonyms_word_filter["en_synonyms"].values[0].split(", ")))
  
  return synonyms
  

def substitute_rw_words(sentence:str):
  """
  get new sentences for each synonym
  steps:
    1. loop in all words
    1.1 get all rw synonyms
    1.2 substitute
  """
  words = str(sentence).split()
  sentences = [sentence]
  for word in words:
    synonyms_rw = get_rw_synonyms(word)
    temp = [] 
    for syn in synonyms_rw:
      if syn!=None:
        temp.append(re.sub(word, str(syn), sentence))
    sentences.extend(temp)
  return sentences

def substitute_en_words(sentence:str):
  """
  get new sentences for each synonym
  steps:
    1. loop in all words
    1.1 get all en synonyms
    1.2 substitute
  """
  words = str(sentence).split(" ")
  sentences = [sentence]
  tokens = nltk.word_tokenize(sentence, preserve_line=True)
  tagged_tokens = nltk.pos_tag(tokens)

  for i, (token, tag) in enumerate(tagged_tokens):
    # print(token)
    # try:
    #   if token in words and tagged_tokens[i+1][0]=="n't": 
    #     # print(token, tagged_tokens[i+1][0])
    #     continue
    #   elif token not in words:
    #     continue
    #   else: pass
    # except:
    #   continue
    if tag.startswith("V") or tag.startswith("N") or tag.startswith("J"):
      synonyms_en = get_en_synonyms(token)
      temp = []
      for syn in synonyms_en:
        temp.append(re.sub(r"\b"+token+"\b", str(syn), sentence))
      sentences.extend(temp)
        
  # if len(sentences)>random_k:
    # return random.sample(sentences, k=random_k)
  return sentences

def substitute_parallel(row):
  en_subs = substitute_en_words(row["en"])
  rw_subs = substitute_rw_words(row["rw"])
  combinations = list(set(itertools.product(en_subs, rw_subs)))
  return combinations

if __name__ == '__main__':
    corpus = []
    
    print('Starting substituting dataset')
    for index, row in data_df[:].iterrows():
        corpus.extend(substitute_parallel(row.astype(str)))
        
        if index%2000==0:
            print(f'\t{index} rows finished substituted')
    
    print('Finished substituting.\n')
    
    df = pd.DataFrame(corpus, columns=columns)
    df.drop_duplicates(inplace=True)
    
    df.to_csv(save_file, index=False)
    
    # with open(en_train_data, 'w', encoding='utf8') as f:
      # f.write("\n".join(df["en"].astype("str").tolist()))
    
    # with open(rw_train_data, 'w', encoding='utf8') as f:
      # f.write("\n".join(df["rw"].astype("str").tolist()))