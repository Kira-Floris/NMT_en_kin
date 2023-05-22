import fitz
import re
import numpy as np
import pandas as pd
import itertools
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk.corpus import gutenberg

pdf_file = 'data/files/unclean/english-kinyarwanda dictionary.pdf'
save_file = 'data/files/clean/en-rw-dictionary.csv'
corpus_pattern = "(.*)\s-\s(.*)"
corpus_split_text = "this book will be of some use to those beginning their study of Kinyarwanda."
en_pattern = r'\s\([^)]*\)'
rw_pattern = r'\s\([^)]*\)'
brackets_pattern = r"\([^\)]+\)"
hyphen_pattern = r'\s-\w+(?:,)?\s*'
semicolon_pattern = r';\s*'

class EnKinExtractor:
  def __init__(
      self, 
      file_path:str=pdf_file,
      save_file:str=save_file,
      corpus_pattern:str=corpus_pattern,
      corpus_start_text:str=corpus_split_text,
      en_pattern:str=en_pattern,
      rw_pattern:str=rw_pattern,
      ):
    self.file_path = file_path
    self.save_file = save_file
    self.corpus_pattern = corpus_pattern
    self.corpus_start_text = corpus_start_text
    self.en_pattern = en_pattern
    self.rw_pattern = rw_pattern
    self.corpus_list = []

    # loading gutenberg
    nltk.corpus.gutenberg.ensure_loaded()
    self.gutenberg_words = gutenberg.words()
    self.gutenberg_freq_dist = nltk.FreqDist(self.gutenberg_words)

    self.__extract_dictionary()
    self.__save_dictionary()

  def __open_file(self):
    with fitz.open(self.file_path) as doc:
      text = ''
      for page in doc:
        text += page.get_text()
    self.doc = text
    return self.doc
  
  def __get_corpus(self):
    corpus = self.doc.split(self.corpus_start_text)[1]
    self.corpus_doc = re.findall(self.corpus_pattern, corpus)
    return self.corpus_doc

  def __process_english(self, text):
    text = re.sub(self.en_pattern, '', text)
    text = self.__process_text(text).split(',')[0]
    return text if text!='' else None

  def __process_kinyarwanda(self, text):
    text = re.sub(self.rw_pattern, '', text)
    text = self.__process_text(text)
    return text if text!='' else None

  def __process_text(self, text):
    # remove words in brackets
    text = re.sub(brackets_pattern, '', text)
    text = text.split('(')[0]

    # replace ; with ,
    text = re.sub(semicolon_pattern, ',', text)

    # remove words that starts with -
    text = re.sub(hyphen_pattern, '', text)

    # remove e.g. 
    def has_eg(sentence):
      pattern = r'e\.g\.'
      return bool(re.search(pattern, sentence))
    
    text = text if has_eg(text)!=True else ''
    return text

  def __extract_rw_synomyms(self, text):
    if len(text.split(','))>0:
      temp = text.split(',')
      return [temp[0], ','.join(temp[1:])]
    else:
      return list(text, None)

  def __get_word_frequency(self, word):
    frequency = self.gutenberg_freq_dist[word]
    return frequency

  def __extract_en_synonyms(self, text, remove_unsimilar=True, remove_single_letter=True):
    synonyms = []
    for syn in wordnet.synsets(text):
      for lemma in syn.lemmas():
          synonyms.append(lemma.name())
    synonyms = list(set(synonyms))

    text_frequency = self.__get_word_frequency(text)
    synonyms_ = []

    # remove words that does not a frequency of text_frequency -150 or above
    # remove words with less than 2 words, eg: I, u, he, me
    if remove_unsimilar and len(text)>2:
      for word in synonyms:
        if text=="lime":
          print(word.split())
        if self.__get_word_frequency(word) >= (text_frequency-150) and len(word.split("_"))==1:
          synonyms_.append(word)
    

    if text in synonyms_:
      synonyms_.remove(text)
    if len(synonyms_)>0:
      temp = re.sub('_',' ',', '.join(map(str, synonyms_)).lower())
      return [text, temp]
    else:
      return [text, None]

  def __generate_word_type(self, en, rw):
    checknoun = wordnet.synsets(en, pos=wordnet.NOUN)
    checkverb = wordnet.synsets(en, pos=wordnet.VERB)
    checkadj = wordnet.synsets(en, pos=wordnet.ADJ)
    if checknoun and checkverb:
      if(rw[0] in ['a','e','i','o','u']):
        return "NOUN"
      else:
        return "VERB"
    if checknoun:
      return "NOUN"
    if checkverb:
      return "VERB"
    if checkadj:
      return "ADJ"
    return None

  def __extract_dictionary(self):
    self.__open_file()
    self.__get_corpus()
    for i in range(len(self.corpus_doc)):
      item = self.corpus_doc[i]
      en_text = self.__process_english(item[0])
      rw_text = self.__process_kinyarwanda(item[1])
      if en_text and rw_text and len(re.findall('-', en_text+rw_text))==0:
        temp = []
        rw_synonyms = self.__extract_rw_synomyms(rw_text.lower())
        en_synonyms = self.__extract_en_synonyms(en_text.lower())
        temp.extend(en_synonyms)
        temp.extend(rw_synonyms)
        self.corpus_list.append(temp) 
    return self.corpus_list

  def __save_dictionary(self):
    self.df = pd.DataFrame(self.corpus_list, columns=['en', 'en_synonyms', 'rw', 'rw_synonyms'])
    # self.df["word_type"] = self.df.apply(lambda x: self.__generate_word_type(x["en"], x["rw"]), axis=1)
    self.df.to_csv(self.save_file, index=False)
    return self.df

if __name__ == '__main__':
    obj = EnKinExtractor()