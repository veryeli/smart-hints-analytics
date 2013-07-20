mport string
import sys
import json

for line in sys.stdin:
    # split line to look for vid more easily
    try:
        user = line.split('\t')[0]
        data = json.loads(line.split('\t')[1])
        print string.join(
            [str(i) for i in [
                user,
                data["correct"],
                data["exercise"],
                data["problem_type"],
                data['attempts'],
                data['count_hints'],
                data['seed'],
                data['problem_number']
            ]], '\x01')
    except:
        pass

