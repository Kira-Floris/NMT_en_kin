# preprocessing data
onmt_preprocess -train_src NMT_en_kin/data/train/train.rw -train_tgt NMT_en_kin/data/train/train.en -valid_src NMT_en_kin/data/dev/dev.rw -valid_tgt NMT_en_kin/data/dev/dev.en -save_data NMT_en_kin/data/vocab/onmt-v1/kin_en

# training
onmt_train --data NMT_en_kin/data/vocab/onmt-v1/kin_en --save_model NMT_en_kin/models/onmt_v1/kin_en_model --world_size 1 --gpu_ranks 0 --train_steps 20000

# testing
onmt_translate --model NMT_en_kin/models/onmt_v1/kin_en_model_step_20000.pt --src NMT_en_kin/data/test/test.rw --output NMT_en_kin/temp/pred_en.txt --replace_unk --verbose

# calculating score
sacrebleu NMT_en_kin/data/test/test.en < NMT_en_kin/temp/pred_en.txt