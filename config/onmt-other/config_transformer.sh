# build vocab
onmt_build_vocab -config NMT_en_kin/config/onmt-other/config_transformer.yaml -n_sample 100000

# train
onmt_train -config NMT_en_kin/config/onmt-other/config_transformer.yaml

# test
onmt_translate -model NMT_en_kin/models/onmt_others/en_kin_model_transformer/en_kin_model_step_12000.pt -src NMT_en_kin/data/test/test-en.txt -output NMT_en_kin/temp/pred_rw.txt -gpu 0 -verbose

# bleu
sacrebleu NMT_en_kin/data/test/test-rw.txt < NMT_en_kin/temp/pred_rw.txt