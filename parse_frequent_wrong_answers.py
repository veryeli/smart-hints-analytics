from collections import defaultdict
import string


def get_common_perseus_hints():
    f = open('/home/analytics/kadata/tmp/hints/khanex-frequent.txt', 'r')

    last_seen = ''
    common_answers = defaultdict(list)
    for line in f:
        if last_seen == '':
            last_seen = line
        elif line == '\n':
            last_seen = ''
        else:
            common_answers[last_seen].append(
                [int(line.split()[-1]), string.join(line.split()[:-1], '')])

    requests = []
    for d in common_answers:
        # make sure it's a perseus exercise
        if '-x' in d:
            request = []
            id = d.strip().split('-')[-1]
            request.append('/api/v1/assessment_items/%s/wrong_answers' % id)
            total_responses = sum(
                [response[0] for response in common_answers[d]])

            # make a dictionary with all responses that account for at least
            # five percent of the incorrect responses
            data = {}
            for response in common_answers[d]:
                if float(response[0] * 100) / total_responses > 5:
                    data[response[1]] = int(
                        float(response[0] * 100) / total_responses)
            request.append(data)
            requests.append(request)
    f.close()
    return requests
