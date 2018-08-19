from collections import Counter
import csv
import subprocess
import inflect

infl_eng = inflect.engine()

def read(fname):
	p = subprocess.Popen(['gunzip', '-c', fname], stdout=subprocess.PIPE)
	for line in p.stdout:
		yield line
	p.wait()
		

def tokenize(fh):
	sent = []
	for line in fh:
		line = line.strip().split()
		if not line:
			if sent:
				yield sent
			sent = []
		else:
			sent.append(line)
	yield sent


def write_to_csv(sents, fname = "deps.csv", mode = "w"):

	with open(fname, mode) as f:
		
		writer = csv.writer(f, delimiter=',')
		
		for s in sents:
		
			writer.writerow(s)
