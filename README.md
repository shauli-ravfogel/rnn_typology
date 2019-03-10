# RNNs and syntactic variability

This repository contains the code for the creation of synthetic langauges used in the paper "Studying the inductive biases of RNNs
with synthetic variations of natural languages" (accepated paper in NAACL 2019).

### Dataset Creation

The `dataset_creation` directory contains the code for creating an agreement dataset for synthetic version of English.

The arguments specified in `main.py` allow controlling for various parameters, such as with which arguments the verb agrees, whether NPs are marked for nuclear cases, which case system to use, and what would be the verb-subject-object order. For an explanation on the command line arguments, run `python main.py -h` from the dataset_creation directory.

Running `main.py` would generate a file that contains instances of modified sentences exhibiting the desired grammatical phenomena. The dataset would be saved in a `datasets` directory.

### Model

The `model` repository contains the code for running the model used in the paper. Running instructions:

1. create train, dev and test agreement datasets.
2. Run the script `collect_vocab.py` from within the `model` directory.
3. Run `main.py`to train the model.
