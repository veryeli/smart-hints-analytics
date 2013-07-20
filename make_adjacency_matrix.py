import string
import pickle
from collections import defaultdict, Counter

f=open('negnums', 'r')
out=open('feature_matrix', 'w')
lines = [line.split('\x01') for line in f]

USER=0
CORRECT=1
ANSWERS=4
HINTS=5
SEED=6
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
    if not line[CORRECT] and (line[HINTS] == 0 or (len(line[ANSWERS]) > 1 and line[ANSWERS][0] != line[ANSWERS][-1])):
        wrong_answers[line[SEED]][line[ANSWERS][0]] += 1

encodings = []


i=0
for pnum in wrong_answers:
    for item in  wrong_answers[pnum].most_common(4):
        encodings.append((pnum, item[0], i))
        i += 1
    encodings.append((pnum, 'correct', i))
    i += 1
    encodings.append((pnum, 'other', i))
    i += 1

encodings_dict = {}
for item in encodings:
    k = str(item[0]) + item[1]
    encodings_dict[k] = item[2]


users = []
current_user = ''
user_vector = []
j=0
for line in lines:
    j += 1
    if line[USER] != current_user:
        if len(user_vector) > 0 and j < 201:
            users.append(user_vector)
        j=0
        current_user = line[USER]
        user_vector = [0 for i in range(200 * NUM_FEATURES)]
    k = str(line[SEED])+ str(line[ANSWERS][0].encode('ascii', 'ignore'))
    if k in encodings_dict:
        user_vector[encodings_dict[k]] = 1
    elif line[CORRECT] == True:
        k = str(line[SEED])+ 'correct'
        user_vector[encodings_dict[k]] = 1
    else:
        k = str(line[SEED])+ 'other'
        user_vector[encodings_dict[k]] = 1

for user in users:
    out.write(string.join([str(i) for i in user], ','))
    out.write('\n')

adjs = np.zeros((1200,1200))

for i in range(len(users)):
    responses = users[i]
    for r1 in responses:
        for r2 in responses:
            if r1 != r2:
                adjs[r1,r2] += 1
                adjs[r2,r1] += 1

np.savez(open('adjacencies.npz', 'w'), adjacencies)
for i in range(len(adjacencies)):
    reg_adjacencies[i] = adjacencies[i]/sum(adjacencies[i])

