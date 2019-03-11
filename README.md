# RNNs and syntactic variability

This repository contains the code for the creation of the synthetic langauges used in the paper "Studying the inductive biases of RNNs
with synthetic variations of natural languages" (accepated paper in NAACL 2019).

### Dataset Creation

The `dataset_creation` directory contains the code for creating verb-argument agreement datasets for synthetic versions of English.

The arguments specified in `main.py` allow controlling for various parameters, such as with which arguments the verb agrees, whether NPs are marked for nuclear cases, which case system to use, and what would be the verb-subject-object order. For example, the input sentence "they say the broker took them out for lunch frequently", when converted to OVS word order, yields the sentence "them took out frequently the broker for lunch say they".

For an explanation on all command line arguments, run `python main.py -h` from the `dataset_creation` directory.

Running `main.py` would generate a dataset file that contains instances of modified sentences exhibiting the desired grammatical phenomena, alongside the agreement patterns in them. This dataset would be saved in a `datasets` directory.

### Model

The `model` repository contains the code for running the model used in the paper. Running instructions:

1. create train, dev and test agreement datasets.
2. Run the script `collect_vocab.py` from within the `model` directory.
3. Run `main.py`to train the model.
