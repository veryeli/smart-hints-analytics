import string
import pickle
from collections import defaultdict, Counter
import numpy as np

f = open('negnums', 'r')
out = open('feature_matrix', 'w')
lines = [line.split('\x01') for line in f]

USER = 0
CORRECT = 1
ANSWERS = 4
HINTS = 5
SEED = 6
NUM_FEATURES = 6
NUM_WRONG_ANSWERS = 4
for line in lines:
    line[CORRECT] = eval(line[CORRECT])
    line[HINTS] = eval(line[HINTS])
    line[SEED] = eval(line[SEED])
    line[ANSWERS] = eval(line[ANSWERS])
pickle.dump(lines, open('picklednegnums', 'w'))

wrong_answers = defaultdict(Counter)


for line in lines:
    if not line[CORRECT] and (
        line[HINTS] == 0 or (
            len(line[ANSWERS]) > 1 and line[ANSWERS][0] != line[ANSWERS][-1])):
        wrong_answers[line[SEED]][line[ANSWERS][0]] += 1

encodings = []

i = 0
problem_id_mappings = {}
for pnum in wrong_answers:
    for item in wrong_answers[pnum].most_common(4):
        encodings.append((pnum, item[0], i))
        problem_id_mappings[i] = pnum
        i += 1
    encodings.append((pnum, 'correct', i))
    problem_id_mappings[i] = pnum
    i += 1
    encodings.append((pnum, 'other', i))
    problem_id_mappings[i] = pnum
    i += 1

encodings_dict = {}
for item in encodings:
    k = str(item[0]) + item[1]
    encodings_dict[k] = item[2]

users = []
current_user = ''
user_vector = []
j = 0
for line in lines:
    j += 1
    if line[USER] != current_user:
        if len(user_vector) > 0 and j < 201:
            users.append(user_vector)
        j = 0
        current_user = line[USER]
        user_vector = []
    k = str(line[SEED]) +    str(line[ANSWERS][0].encode('ascii', 'ignore'))
    if k in encodings_dict:
        user_vector.append(encodings_dict[k])
    elif line[CORRECT]:
        k = str(line[SEED]) + 'correct'
        user_vector.append(encodings_dict[k])
    else:
        k = str(line[SEED]) + 'other'
        user_vector.append(encodings_dict[k])

for user in users:
    out.write(string.join([str(i) for i in user], ','))
    out.write('\n')

adjacencies = np.zeros((1200, 1200))

for i in range(len(users)):
    print i
    responses = users[i]
    for r1 in responses:
        for r2 in responses:
            if r1 != r2:
                adjacencies[r1, r2] += 1
                adjacencies[r2, r1] += 1

np.savez(open('adjacencies.npz', 'w'), adjacencies)
for i in range(len(adjacencies)):
    adjacencies[i] = adjacencies[i]/sum(adjacencies[i])

reverse_mappings = {}
for item in encodings_dict:
    reverse_mappings[encodings_dict[item]] = item


def print_graph(limit, outfile):
    outfile.write('digraph G {\nsize="5";\n')
    for i in range(len(adjacencies)):
        if i % 6 < 3:
            for j in range(i):
                if adjacencies[i, j] > limit:
                    print reverse_mappings[i], reverse_mappings[j]
                    outfile.write(
                        '%s->%s;\n' % (
                            problem_id_mappings[i], problem_id_mappings[j]))
    outfile.write('}')

print_graph(.005, open('connections.gv', 'w'))
