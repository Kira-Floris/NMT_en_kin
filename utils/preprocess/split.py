import pandas as pd
from sklearn.model_selection import train_test_split

train_file = 'data/train/'
test_file = 'data/test/'
dev_file = 'data/dev/'

def split(
    file_path="data/files/clean/data-substituted.csv", 
    train_size=0.8, 
    valid_size=0.1, 
    test_size=0.1,
    langs = ['en', 'rw'],
    save_format = '{}.{}'
):
    df = pd.read_csv(file_path)
    
    train, test_valid = train_test_split(df, test_size=1-train_size, random_state=42)
    test, valid = train_test_split(test_valid, test_size=valid_size/(valid_size+test_size))
    
    for lang in langs:
        # training files
        with open(train_file+save_format.format('train', lang), 'w', encoding='utf-8') as f:
            f.write('\n'.join(train[lang].tolist()))
        
        # testing files
        with open(test_file+save_format.format('test', lang), 'w', encoding='utf-8') as f:
            f.write('\n'.join(test[lang].tolist()))
        
        # validation files
        with open(dev_file+save_format.format('dev', lang), 'w', encoding='utf-8') as f:
            f.write('\n'.join(valid[lang].tolist()))
            
if __name__=='__main__':
    split()
            
