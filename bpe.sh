subword-nmt learn-joint-bpe-and-vocab -s 4000 --input data/train.en data/train.kin --output bpe.4000.codes --write-vocabulary data/vocab.en data/vocab.kin

# subword-nmt learn-joint-bpe-and-vocab -s 4000 --input train.kin --output train.bpe.kin --write-vocabulary vocab.kin