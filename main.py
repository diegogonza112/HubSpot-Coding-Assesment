import json

import requests as re

url_get = 'https://candidate.hubteam.com/candidateTest/v3/problem/dataset?' \
          'userKey=49fc5af6319c1dac88df38fdde57'

url_post = 'https://candidate.hubteam.com/candidateTest/v3/problem/result?' \
           'userKey=49fc5af6319c1dac88df38fdde57'

information = re.get(url=url_get)
info_dict = information.json()
times = []
users = []
page_time = {}
users_pages = {}

for info in info_dict['events']:
    # create list of user ids, sorted times, and a dictionary where the key is
    # the userid and the info is a list of lists of a page visit and the time
    users.append(info["visitorId"])
    times.append(info['timestamp'])
    if info["visitorId"] in users_pages:
        users_pages[info["visitorId"]].append([info['url'], info['timestamp']])
    else:
        users_pages[info["visitorId"]] = [[info['url'], info['timestamp']]]

times.sort()  # sorted in order to search times in order; increases
# simplicity for ordering events (even if the run time is affected)

output_dict = {"sessionsByUser": {}}


def populate_output():
    for u in users:
        # populates the output dictionary
        output_dict["sessionsByUser"][u] = create_smallest_dict(u)


def create_smallest_dict(user):  # list of creates the smallest nested
                                 # dictionary
    out = []
    previous = 0
    for t in times:
        for i in users_pages[user]:
            if t - previous <= 600000 and i[-1] == t:
                # checks if previous
                # event was less than 10 minutes before
                out[-1]["duration"] += (t - previous)
                out[-1]["pages"].append(i[0])
                previous = t  # sets new time to check as most recent time
            elif i[-1] == t:
                output = {
                    "duration": 0,
                    "pages": [i[0]],
                    "startTime": t
                }
                out.append(output)
                previous = t
    return out


def main():
    populate_output()
    return re.post(url=url_post, data=json.dumps(output_dict))


main()
