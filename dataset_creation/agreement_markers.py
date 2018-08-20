#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
An abstract class that adds agreement and case marks to sentence elements (verbs and their arguments).

Case system:

						SG			PL
	
	SUBJECT/ERGATIVE			§			©
	
	OBJECT/ABSOLUTIVE			#			*
	
	INDIRECT OBJECT / DATIVE		@			&
"""

class AgreementMarker(object):

	def __init__(self, add_cases):
	
		"""
		
		:param add_cases:
		
			a boolean. If true, adds case suffixes to NPs.
		"""
		
		self.add_cases = add_cases
		
	def mark(self, verb_node, agreement_nodes):
	
		cases = []
		is_transitive = any((n.label == "dobj" for n in agreement_nodes))
		verb_suffix = ""
		
		for agreement_node in agreement_nodes:
		
			case = self.get_case(verb_node, agreement_node, is_transitive)

			verb_suffix += case
			
			if self.add_cases:
				
				cases.append((agreement_node, case))

		
		verb_suffix = " ".join(sorted(verb_suffix))
		cases.append((verb_node, verb_suffix))

		return cases
			
	def get_case(self, verb_node, agreement_node, is_transitive):
	
		raise NotImplementedError
		
		
class NominativeAcusativeMarker(AgreementMarker):

	def __init__(self, add_cases = False):
		super(NominativeAcusativeMarker, self).__init__(add_cases)
		
	def get_case(self, verb_node, agreement_node, is_transitive):

		if agreement_node.label == "nsubj" or agreement_node.label == "nsubjpass":
				
			case = "§" if agreement_node.number == "sg" else "©"
					
		elif agreement_node.label == "dobj":
			
			case = "#" if agreement_node.number == "sg" else "*"
			
		elif agreement_node.label == "iobj":
			
				
			case = "@" if agreement_node.number == "sg" else "&"
		
		return case
		

		
class ErgativeAbsolutiveMarker(AgreementMarker):

	def __init__(self, add_cases=False):
		super(ErgativeAbsolutiveMarker, self).__init__(add_cases)
		
	def get_case(self, verb_node, agreement_node, is_transitive):

		is_subj = agreement_node.label == "nsubj" or agreement_node.label == "nsubjpass"
		
		if (not is_transitive and is_subj) or agreement_node.label == "dobj":
				
			case = "#" if agreement_node.number == "sg" else "*"
					
		elif is_transitive and is_subj:
			
			case = "§" if agreement_node.number == "sg" else "©"
			
		elif agreement_node.label == "iobj":
			
				
			case = "@" if agreement_node.number == "sg" else "&"
		
		return case
		
