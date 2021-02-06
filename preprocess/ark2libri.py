# -*- coding: utf-8 -*- #
"""*********************************************************************************************"""
#   FileName     [ ark2libri.py ]
#   Synopsis     [ process the .ark file preprocessed by kaldi for our dataloader ]
#   Author       [ Andy T. Liu (Andi611) ]
#   Copyright    [ Copyleft(c), Speech Lab, NTU, Taiwan ]
#   Reference    [ https://github.com/nttcslab-sp/kaldiio ]
"""*********************************************************************************************"""

###############
# IMPORTATION #
###############
import os
import pickle
import operator
import numpy as np
import pandas as pd
from tqdm.auto import tqdm
from kaldiio import ReadHelper


############
# SETTINGS #
############
DATA_TYPE = 'fmllr' # this can be either ['mfcc', 'fbank', 'fmllr']
KALDI_ROOT = '/media/andi611/1TBSSD/kaldi/' # change this to your own kaldi root
LIBRI_PATH = os.path.join(KALDI_ROOT, 'egs/librispeech/s5/' + DATA_TYPE + '_cmvn/') # this needs to be generated by the scripts `dump_fmllr_cmvn.sh` or `dump_mfcc_cmvn.sh`
OUTPUT_DIR = '../data/libri_' + DATA_TYPE + '_cmvn' # 


############
# CONSTANT #
############
SETS = ['dev_clean', 'test_clean', 'train_clean_100', 'train_clean_360', 'train_other_500'] # you should not need to change this


########
# MAIN #
########
def main():
    if not os.path.isdir(KALDI_ROOT):
        print('CHANGE THIS TO YOUR OWN KALDI ROOT: ', KALDI_ROOT)
        exit()

    if not os.path.isdir(LIBRI_PATH):
        print('Invalid path for the kaldi librispeech dataset: ', LIBRI_PATH)
        print('Please run the kaldi scripts first! More information are described in the README file and Wiki page.')

    if not os.path.isdir(OUTPUT_DIR):
        os.mkdir(OUTPUT_DIR)

    # read data from the preprocessed kaldi directory
    for s in SETS:
        with ReadHelper('ark:' + LIBRI_PATH + s + '/' + DATA_TYPE + '_cmvn.ark') as reader:
            
            output = {}
            print('Preprocessing', s, 'data...')

            cur_dir = os.path.join(OUTPUT_DIR, s.replace('_', '-'))
            if not os.path.isdir(cur_dir): os.mkdir(cur_dir)

            for key, array in tqdm(reader):

                array = np.asarray(array).astype('float32')
                np.save(os.path.join(cur_dir, key), array)
                output[os.path.join(s.replace('_', '-'), key + '.npy')] = len(array)

            output = sorted(output.items(), key=operator.itemgetter(1), reverse=True)
            df = pd.DataFrame(data={'file_path':[fp for fp, l in output], 'length':[l for fp, l in output], 'label':'None'})
            df.to_csv(os.path.join(OUTPUT_DIR, s.replace('_', '-') + '.csv'))

    print('[ARK-TO-LIBRI] - All done, saved at \'' + str(OUTPUT_DIR) + '\', exit.')
    exit()

if __name__ == '__main__':
    main()
    
