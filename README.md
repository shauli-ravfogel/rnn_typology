# rnn_typology

This repository contains the code for the creation of synthetic langauges used in the paper "Studying the inductive biases of RNNs
with synthetic variations of natural languages" (accepated paper in NAACL 2019).

### Dataset Creation

The `dataset_creation` directory contains the code for creating an agreement dataset for synthetic version of English.

The arguments specified in `main.py` allow controlling for various parameters, such as with which arguments the verb agrees, whether NPs are marked for nuclear cases, which case system to use, what would be the verb-subject-object order. For an explanation on the command line arguments, run `python main.py -h` from the dataset_creation directory.

Running `main.py` would generate a file that contains instances of modified sentences exhibiting the desired grammatical phenomena. 
