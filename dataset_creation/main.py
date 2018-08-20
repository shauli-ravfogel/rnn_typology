from utils import *
import agreement_collector
import agreement_markers


if __name__ == "__main__":

	#agreement_marker = agreement_markers.NominativeAcusativeMarker(add_cases = False)
	agreement_marker = agreement_markers.ErgativeAbsolutiveMarker(add_cases = True)
	agreements =  {"nsubj": True, "dobj": True, "iobj": True}
	
	collector = agreement_collector.AgreementCollector(skip = 5, agreement_marker = agreement_marker, order = "vos", agreements = agreements, most_common = 200000, mark_verb = True,  fname = "wiki.parsed.subset.50.lemmas.zip")
	
	collector.collect_agreement()
