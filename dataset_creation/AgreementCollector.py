#!/usr/bin/env python
# -*- coding: utf-8 -*-

from utils import *
from collections import defaultdict
import random
import time
import agreement_markers
import csv

INDEX = 0
WORD = 1
LEMMA = 2
POS = 3
PARENT_INDEX = -4
LABEL = -3
PARENT = -1


"""
This classs represents a node in a dependency parse tree. It offers methods for traversing the subtree rooted in the node in a specific order, finding the number of a NP node and collecting verb arguments.
"""

class Node(object):

	def __init__(self, tok_id, word, lemma, pos, label):
	
		
		self.tok_id = tok_id
		self.word = word
		self.lemma = lemma
		self.pos = pos
		self.label = label
		self.is_verb = self.pos.startswith("V")
		
		self.children = []
		
		self.parent = None
		self.parent_index = None
		self.number = None
		
		self.root = False
		self.depth = 0
		
		
	def __str__(self):
	
		"""
		print the subtree rooted in self with indentation to express hierarchical sturcture.
		
		return: a string representing the sentence rooted in self.
		"""
		
		parent = self.parent_index if self.parent_index else "ROOT"
		s =  " "*self.depth + str(self.tok_id)+"\t"+self.word+"\t"+self.lemma+"\t"+self.pos+"\t"+self.label+"\t"+str(parent)+"\n"
		for child in self.children:
			s += str(child)
			
		if self.root: s = s.strip()
		
		return s
		
	def get_tree_structure(self):
	 
	 	pass
		
	
	def size(self):
	
		"""
		return: number of nodes rooted in self.
		"""
		
		if not self.children: 
			return 1
		
		children_size = [c.size() for c in self.children]
		
		return sum(children_size) + 1
		
	def get_index(self): return self.tok_id

		
	def dfs(self, order = None):
	
		"""
		perform a DFS traversal over the subtree rooted in self, in a spcific order.
		
		:param order:
				a string, representing the subject-object-verb order of the traversal, e.g. sov, vos.
				if none, assumes a canonical order.
		
		:return:
			a tuple (path, tree_structure):	
				path:
					an ordered list containing the nodes visited during the traversal.			
				tree_structure:
				
					a list containing a nested parantheses strings representing sentence structure
					e.g. ["(", "(", "The", "man", ")", ...]	
		"""
		
		nodes_sorted = sorted(self.children+[self], key = lambda node: node.get_index())
		nodes_in_order = nodes_sorted # the sentence tree is constructed in such a way that performing a DFS on the nodes ordered by their index yields the original linear order of elements.
		
		
		if self.is_verb and order is not None:

			# if the node represents a verb, reorder its children to express the desired word order.
			
			node_to_char = lambda n: "v" if n.is_verb else "s" if (n.label == "nsubj" or n.label == "nsubjpass") else "o" 
		
			labels = set(["nsubj", "nsubjpass", "dobj"])
			
			# find correct order for subject, object and verb nodes.
			
			all_elements = [n for n in self.children if n.label in labels]
			all_elements.append(self)
			all_elements = set(all_elements)
			
			all_elements_sorted = sorted(all_elements, key = lambda n: order.index(node_to_char(n)))
	
			j = 0
			
			# change nodes_in_order ordering to correct order.
			
			for i, n in enumerate(nodes_in_order):
			
				if n in all_elements:
				
					nodes_in_order[i] = all_elements_sorted[j]
					j += 1

		
		# traverse the ordered nodes.
		
		path = []
		tree_structure = ["("]
		
		for n in nodes_in_order:
		
			if n is not self:
			
				child_nodes, child_subtree = n.dfs(order)
				tree_structure.extend(child_subtree)
				path.extend(child_nodes)
			else:
			
				path.append(self)
				tree_structure.append(self.word)
				
		tree_structure.append(")")

		return path, tree_structure
				
		
	def add_children(self, children, edges, tree):
	
		"""
			add children nodes to this node's list of children.
			
			:param children:
					a list, containing index of children nodes
				
			:param edges:
					a dictionary, mapping node_id to a list of its children ids.
				
			:param tree:
					a dictionary, mapping node ids to node objects
				
		"""
		
		for tok_id in children:
		
			child = tree[tok_id]
			child.depth = self.depth + 1
			self.children.append(child)
				
			child.add_children(edges[tok_id], edges, tree)
			child.add_parent(self)
			
		
	def add_parent(self, node):

		self.parent = node
		self.parent_index = node.tok_id
			

	def set_number(self):
	
		"""
			set self number according to word form and POS.
		"""
		
		word, pos = self.word, self.pos
		
		word = word.lower()
		num = ""
		
		#print word, pos, self.root
		
		if not (pos in  ["NN", "NNP", "NNS", "NNPS", "PRP"] or word in ["this", "that", "these", "those", "which", "who"]):
			self.number = None
			return
		
		if pos == "NN" or pos == "NNP": 
			num =  "sg"
		
		elif pos == "NNS" or pos == "NNPS": 
			num =  "pl"
		
		elif pos == "DT":
		
			if word in ["this", "that"]: num = "sg"
			else: num = "pl"
			
		elif pos == "PRP":

			if word in ["he", "him", "she", "her", "i", "it", "me"]:
				num = "sg"
			elif word in ["they", "we", "us", "them"]:
				num = "pl"
			else: # you
				num = None
			
		elif pos == "WP" or pos == "WDT":
			
			# for who/which, check the referent's number.
			
			# parsing error
			
			if self.parent is None or self.parent.parent is None: 
			
				self.number = None
				return
			
			grandparent_pos = self.parent.parent.pos
			
			if grandparent_pos == "NN" or grandparent_pos == "NNP" or grandparent_pos in ["this", "that"]:
				num = "sg"
			num =  "pl"
		
		self.number = num

	
	def collect_arguemnts(self, agreement_dict, agreements_to_collect):


		if self.is_verb:
		
			
			nuclear_children = (c for c in self.children if c.label in agreements_to_collect and c.pos in ["NN", "NNP", "NNS", "NNPS", "PRP", "WDT", "WP", "DT"])
			
			for c in nuclear_children:
				
				if c.pos=="WDT" or c.pos=="WP" and self.label!="rcmod":
					return {}
				
				if c.number is None: return {}
					
				agreement_dict[self.get_index()].append(c)

		for c in self.children:
		
			c.collect_arguemnts(agreement_dict, agreements_to_collect)
		
		return agreement_dict


class AgreementCollector(object):

	def __init__(self, skip = 5, fname = "wiki.parsed.subset.50.lemmas.zip", order = "svo", agreement_marker = None, agreements = {}, most_common = 10000):
	
		self.skip = skip
		self.fname =  fname
		self.order = order
		self.agreement_marker = agreement_marker
		self.agreements = agreements
		self.most_common = most_common
		self._load_freq_dict()
		
		if isinstance(agreement_marker, agreement_markers.ErgativeAbsolutiveMarker) and not agreements['dobj']:
			
			raise Exception("Ergative-absolutive implies verb-obj agreement")
	
	def _load_freq_dict(self):
	
		vocab = set()
		
		with open("vocab.txt", "r") as f:
		
			lines = f.readlines()
			
		for i, line in enumerate(lines):
		
			word, pos, freq = line.strip().split("\t")
			vocab.add(word)
			
			if i > self.most_common:
			
				break
				
		self.vocab = vocab
		
	def _sent_to_tree(self, sent):
	
		"""
		convert a sentence to a rooted tree object.
		"""
		
		tree = dict()
		edges = defaultdict(list)
	
		for tok in sent:
		
			tok_id, word, lemma, pos, label, parent = int(tok[INDEX])-1, tok[WORD], tok[LEMMA], tok[POS], tok[LABEL], int(tok[PARENT_INDEX]) - 1
	
			node = Node(tok_id, word, lemma, pos, label)
			
			if label == "ROOT":
				root = node
				node.root = True
				tree['root'] = node
				root_id = tok_id
			
			tree[tok_id] = node
			edges[parent].append(tok_id)
		
		for node in tree.values():
			node.set_number()
			
		root_children = edges[root.tok_id]
		root.add_children(root_children, edges, tree)
		
		return tree
	
	def _get_nodes_between(self, node1_index, node2_index, dfs_ordered_nodes): # in dfs order
	
		
		if node2_index < node1_index:
		
			node2_index, node1_index = node1_index, node2_index
		
		
		return dfs_ordered_nodes[node1_index + 1 :node2_index]
		
		
	def _get_tree_and_deps(self, sent):
	
		tree = self._sent_to_tree(sent)
		root = tree['root']
		
		
		for n in tree.values():
			
			
			n.word = n.word.lower()
	
			if n.word not in self.vocab:
			
				n.word = n.pos
	
		agreement_dict = defaultdict(list)
		agreements_to_collect = [k for (k,v) in self.agreements.items() if v]
		if "nsubj" in agreements_to_collect: agreements_to_collect.append("nsubjpass")
		root.collect_arguemnts(agreement_dict, agreements_to_collect) 
		
		nodes_dfs, tree_structure = root.dfs(self.order)
		
		
		depths = []
		pos_tags = []
		lemmas = []
		labels = []
		
		for n in nodes_dfs:
		
			depths.append(str(n.depth))
			pos_tags.append(n.pos)
			lemmas.append(n.lemma)
			labels.append(n.label)
			
		
		is_rcmod = lambda node: node.label=="rcmod"
		is_subj = lambda node: node.label =="nsubj"
		deps = defaultdict(dict)
		
		for verb_id in agreement_dict.keys():
			
			verb_arguments = agreement_dict[verb_id]
			verb_node = tree[verb_id]
			verb_index = nodes_dfs.index(verb_node)
			
			if self.agreement_marker:
					self.agreement_marker.mark(verb_node, verb_arguments)
							
			for argument_node in verb_arguments:
				
				argument_index = nodes_dfs.index(argument_node)
				
				between = self._get_nodes_between(verb_index, argument_index, nodes_dfs)
				nouns_between = (n for n in between if n.pos in ['NN', 'NNS'])
				dis = len(between) + 1
				has_rel = 1 if any(map(is_rcmod, between)) else 0
				has_subj = 1 if any(map(is_subj, between)) else 0
				num_attractors = len([n for n in nouns_between if n.number != argument_node.number])
				
				label = argument_node.label if argument_node.label != "nsubjpass" else "nsubj"
				
				deps[verb_index][label] = {"index": argument_index, "number": argument_node.number, "distance": str(dis), "has_rel": str(has_rel), "has_subj": str(has_subj), "number_attractors": str(num_attractors), "pos": argument_node.pos}
				
			
		deps = {k:v for (k,v) in deps.iteritems() if "nsubj" in v or "nsubjpass" in v}
	
		words = [n.word for n in nodes_dfs]
		sent_info = (words,lemmas, pos_tags, depths, labels)
		
		return sent_info, deps

		
	def collect_agreement(self):
	
		sents = []
		t = time.time()
		
		batches = 0
		
		for i, sent in enumerate(tokenize(read(self.fname))):
			
			if i % self.skip != 0 and i > 0: continue
			
			if i % 100000 == 0 and i > 0:
				print time.time() - t
				t = time.time()
				print i
				
			sent_info, deps = self._get_tree_and_deps(sent)
			words,lemmas, pos_tags, depths, labels = sent_info
			
			if not deps: continue
			
			verb_index = random.choice(deps.keys())
			verb_dep = deps[verb_index]
			
			sent_dict = {}
			sent_dict["sent_words"] = " ".join(words)
			sent_dict["sent_pos"] = " ".join(pos_tags)
			sent_dict["sent_lemmas"] = " ".join(lemmas)
			sent_dict["sent_labels"] = " ".join(labels)
			sent_dict["sent_depths"] = " ".join(depths)
			sent_dict["verb_index"] = str(verb_index)
			sent_dict["original_sent"] = " ".join([tok[WORD] for tok in sent])

			existing_verb_arguments = {}
					
			props = ["index", "number", "distance", "has_rel", "has_subj", "number_attractors", "pos"]
			
			for l in self.agreements:
				
				for prop in props:
				
					val = verb_dep[l][prop] if l in verb_dep else "-"
					sent_dict[l + "_" + prop] = val
			
			sents.append(sent_dict)
			
			if "a gimbal" in sent_dict["sent_words"]:
			
				for tok in sent:
					print "\t".join(tok)
				print sent_dict["sent_words"]
				print sent_dict["original_sent"]
				exit()
					
			if i % 1000 == 0:
			
				if batches == 0:

					write_to_csv([sents[0].keys()], mode = "w")
				
				else:
					write_to_csv([sent_dict.values() for sent_dict in sents], mode = "a")
					sents = []
					
				batches += 1
					
			
		
			

