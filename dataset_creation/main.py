from utils import *
import AgreementCollector
import agreement_markers


if __name__ == "__main__":

	#agreement_marker = agreement_markers.NominativeAcusativeMarker(add_cases = False)
	agreement_marker = agreement_markers.ErgativeAbsolutiveMarker(add_cases = True)
	agreements =  {"nsubj": True, "dobj": True, "iobj": True}
	
	collector = AgreementCollector.AgreementCollector(skip = 5, agreement_marker = agreement_marker, order = "vos", agreements = agreements, most_common = 200000)
	
	collector.collect_agreement()
