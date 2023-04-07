# build vocab
onmt_build_vocab -config NMT_en_kin/config/onmt-other/config_transformer.yaml -n_sample 100000

# train
onmt_train -config NMT_en_kin/config/onmt-other/config_transformer.yaml