import argparse
import time

input_temp_path = 'NMT_en_kin/utils/onmt/v1/temp/input_'

def translate(
    text: str,
    model_path: str 
):
    # create input file
    input_file = input_temp_path+str(time.time())+'.txt'
    
    return 