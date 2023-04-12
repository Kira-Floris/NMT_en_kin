import argparse
import time
import os

input_temp_path = 'utils/onmt/v1/temp/temp_{}_input.txt'
output_temp_path = 'utils/onmt/v1/temp/temp_{}_output.txt'

def translate(
    text: str,
    model_path: str,
    onmt_version='v1'
):
    """
    implementation steps
        1. create input and output files with timestamp names to differentiate them
        2. translate using onmt_translate what is in input file and output it in output file
        3. read the response in output
        4. delete the temporary files of input and output  
    """
    
    timestamp = str(time.time())
    input_file_path = input_temp_path.format(timestamp)
    output_file_path = output_temp_path.format(timestamp)
    
    os.system(f'echo {text} > {input_file_path}')
    if onmt_version=='v1':
        os.system(f'onmt_translate -model {model_path} --src {input_file_path} --output {output_file_path} -verbose -replace_unk')
    else:
        os.system(f'onmt_translate -model {model_path} -src {input_file_path} -output {output_file_path} -gpu 0 -verbose')    
    response = None
    
    with open(output_file_path, 'r') as out:
        response = out.read()
        print(response)
        out.close()
        
    os.remove(input_file_path)
    os.remove(output_file_path)
    return response