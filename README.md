# Modified_English


### Dataset Creation

The `dataset_creation` directory contains the code for creating a modified-English agreement dataset. To run the code, download the lemmatized and parsed Wikipedia corpus and locate it in the same directory.

The arguments specified in `main.py` allow controlling for various parameters, such as with which arguments the verb agrees, whether NP's are marked for nuclear cases, which case system to use, what would be the verb-subject-object order, etc:

```python
	#agreement_marker = agreement_markers.NominativeAcusativeMarker(add_cases = False)
	agreement_marker = agreement_markers.ErgativeAbsolutiveMarker(add_cases = True)
	agreements =  {"nsubj": True, "dobj": True, "iobj": True}
	
	collector = AgreementCollector.AgreementCollector(skip = 5, agreement_marker = agreement_marker,
  order = "vos", agreements = agreements, most_common = 200000, mark_verb = True)
	
	collector.collect_agreement()
```

Running `main.py` would generate a file named `deps.csv`, that contains instances of modified sentences that present the desired grammatical phenomena. 
