from spellchecker import SpellChecker

spell = SpellChecker()

def correction(text):
    words_list = spell.unknown(list(text.split(' ')))
    
    correction_list = []
    for word in words_list:
        correction_list.append(spell.correction(word))
        
    return ' '.join(correction_list)