#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
An abstract class that adds agreement and case marks to sentence elements (verbs and their arguments).
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
		
		# collect cases for verb arguments.
		
		for agreement_node in agreement_nodes:
		
			case = self.get_case(verb_node, agreement_node, is_transitive)
			cases.append(case)
			
			if self.add_cases:
				
				# add case marking on NPs
				
				if agreement_node.word != agreement_node.pos:
					agreement_node.word = agreement_node.lemma.lower()
					
				agreement_node.word += "!"
				agreement_node.word += case
				
		
		# add verb agreement
		
		verb_and_children = verb_node.children[:]
		verb_and_children.append(verb_node)
		
		# lemmatize verb
		
		for v in verb_and_children:
		
			if not v.is_verb: continue
			
			if v.word in ["was", "were"]:
			
				v.word = "was"
				
			if v.lemma == "have":
				
				v.word = "have"
		
		if (verb_node.pos == "VBZ" or verb_node.pos == "VBP"):
			
			verb_node.word = verb_node.lemma
			
		verb_node.word += "!"
		
		for case in sorted(cases):
			
			verb_node.word += case
			
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
		
