# preprocessing data
onmt_preprocess -train_src NMT_en_kin/data/train/train.en -train_tgt NMT_en_kin/data/train/train.kin -valid_src NMT_en_kin/data/dev/dev.en -valid_tgt NMT_en_kin/data/dev/dev.kin -save_data NMT_en_kin/data/vocab/onmt-v1/en_kin

# training
onmt_train --data NMT_en_kin/data/vocab/onmt-v1/en_kin --save_model NMT_en_kin/models/onmt_v1/en_kin_model --world_size 1 --gpu_ranks 0 --train_steps 20000

# testing
onmt_translate --model NMT_en_kin/models/onmt_v1/en_kin_model_step_20000.pt --src NMT_en_kin/data/test/test.en --output NMT_en_kin/temp/pred_kin.txt --replace_unk --verbose

# calculating score
sacrebleu NMT_en_kin/data/test/test.kin < NMT_en_kin/temp/pred_kin.txt