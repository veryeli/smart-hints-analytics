import re
import ast
import sys
from collections import defaultdict
from collections import Counter
import matplotlib.pyplot as plt
from collections import OrderedDict
import random

d = defaultdict(lambda: defaultdict(int))
non_decimal = re.compile(r'[^\d.-]+')

answer_key = {}
with open("all", "r") as f:
	for line in f.readlines():
		a = line.rstrip('\t\n').split("\x01")
		correct, problem, responses, seed = a[0], a[1], ast.literal_eval(a[2]), a[3]
		responses = set(responses[:-1])
		for response in responses:
			d[(problem, seed)][response] += 1

with open("khanex-frequent.txt", "w") as out:
	for (problem, seed) in d.keys():
		out.write('\n%s-%s\n' % (problem, seed))
		for response in d[(problem, seed)].values():
			out.write("%s %s\n" % (response, d[(problem, seed)][response]))
