# build vocab
onmt_build_vocab -config NMT_en_kin/config/onmt-other/config_transformer_rw_en.yaml -n_sample 100000

# train
onmt_train -config NMT_en_kin/config/onmt-other/config_transformer_rw_en.yaml

# test
onmt_translate -model NMT_en_kin/models/onmt_others/kin_en_model_transformer/kin_en_model_step_12000.pt -src NMT_en_kin/data/test/test-rw.txt -output NMT_en_kin/temp/pred_en.txt -gpu 0 -verbose

# bleu
sacrebleu NMT_en_kin/data/test/test-en.txt < NMT_en_kin/temp/pred_en.txt