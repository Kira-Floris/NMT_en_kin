"""
This is an implementation of word level substitution
by using synonyms for both english and kinyarwanda
"""

import pandas as pd
import numpy as np
import re
import itertools

data_file = 'data/files/clean/data.csv'
dictionary_file = 'data/files/clean/en-rw-dictionary-save.csv'
save_file = 'data/files/clean/data-substituted.csv'
columns = ['en','rw']

dictionary_df = pd.read_csv(dictionary_file)
dictionary_df.dropna(inplace=True)

data_df = pd.read_csv(data_file, encoding='utf-8')

def get_rw_synonyms(word, df=dictionary_df, src='en', tgt='rw'):
  """
  gets synonyms to replace in kinyarwanda column
  """
  synonyms_word_filter = df[df[src]==word]
  synonyms = list(set(list(synonyms_word_filter[tgt])))
  # synonyms = synonyms.append(word)
  return synonyms

def get_en_synonyms(word, df=dictionary_df, src='rw', tgt='en'):
  """
  get synonyms to replace in english column
  """
  synonyms_word_filter = df[df[src]==word]
  synonyms = list(set(list(synonyms_word_filter[tgt])))
  # synonyms = synonyms.append(word)
  return synonyms

def substitute_rw_words(sentence:str):
  """
  get new sentences for each synonym
  steps:
    1. loop in all words
    1.1 get all en words matching rw word in dictionary using get_en_synonyms
    1.2 get the en translations in rw
    1.3 substitute
  """
  words = str(sentence).split()
  sentences = []
  for word in words:
    synonyms_en = get_en_synonyms(word)
    synonyms_rw = [get_rw_synonyms(item) for item in synonyms_en]
    synonyms_rw = list(set(sum(synonyms_rw, [])))
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
    1.1 get all rw words matching en word in dictionary using get_en_synonyms
    1.2 get the rw translations in en
    1.3 substitute
  """
  words = str(sentence).split()
  sentences = []
  for word in words:
    synonyms_rw = get_rw_synonyms(word)
    synonyms_en = [get_en_synonyms(item) for item in synonyms_rw]
    synonyms_en = list(set(sum(synonyms_en, [])))
    temp = []
    for syn in synonyms_en:
      if syn!=None:
        temp.append(re.sub(word, str(syn), sentence))
    sentences.extend(temp)
  return sentences

def substitute_parallel(row):
  en_subs = substitute_en_words(row[0])
  rw_subs = substitute_rw_words(row[1])
  combinations = list(set(itertools.product(en_subs, rw_subs)))
  return combinations

if __name__ == '__main__':
    
    corpus = []
    
    print('Starting substituting dataset')
    for index, row in data_df.iterrows():
        corpus.extend(substitute_parallel((row[1], row[0])))
        
        if index%2000==0:
            print(f'\t{index} rows finished substituting')
    
    print('Finished substituting.\n')
    
    df = pd.DataFrame(corpus, columns=columns)
    df.to_csv(save_file, index=False)