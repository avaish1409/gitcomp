# import statements
# cli args
import argparse
# webscripts
import urllib.request
import json
# tabulation
from prettytable import PrettyTable, ALL
# logging
import logging

# get user or repo data
def user_or_repo(arr, option = 'user'):
    # base url
    if option == 'repo':
        base_url = 'https://api.github.com/repos/'
    else:
        base_url = 'https://api.github.com/users/'

    raw_data = []
    for i in range(len(arr)):
        with urllib.request.urlopen(base_url + arr[i]) as url:
            user_data = json.loads(url.read().decode())
            raw_data.append(user_data)

    return raw_data

# get data of all repo of given user(s)
def all_repo():
    # repo list
    # return list of all repo details
    return

# keep only required user/repo details for comparison
def filter_data(raw_data, option = 'user'):
    if option == 'repo':
        required_data = ['full_name', 'forks', 'open_issues',
                 'watchers', 'network_count', 'subscribers_count']
    else:
        required_data = ['login', 'followers', 'following', 'site_admin',
                 'name', 'company', 'blog', 'location', 'public_repos', 'public_gists']

    details = {}
    for i in required_data:
        temp = []
        for j in raw_data:
            temp.append(j[i])
        details[i] = temp

    return details

# store list to csv file
def create_csv(arr):
    for i in arr:
        print(', '.join(i))
        # print(i)
    return

#Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
  
#Creating an object
logger=logging.getLogger()

# check inout type and run user_or_repo or all_repo
# create parser object
parser = argparse.ArgumentParser(description="A text file manager!")

# defining arguments for parser object
parser.add_argument("-u", "--user", type=str, nargs='*',
                    metavar="user_name", default=None, dest='user_names',
                    help="Opens and reads the specified text file.")

parser.add_argument("-r", "--repo", type=str, nargs='*',
                    metavar="repo", default=None, dest='repo_names',
                    help="Shows all the text files on specified directory path.\
                    Type '.' for current directory.")

parser.add_argument("-o", "--outputtype", type=str, nargs=1,
                    metavar="output_dest", default=['cmd'], dest='out_type',
                    help="Check whether the output should be printed in cmd, csv, html or json.\
                    Type '.' for current directory.")

# parse the arguments from standard input
args = parser.parse_args()

# calling functions depending on type of argument
if args.user_names != None:
    # print('user analysis')
    logger.info("user analysis")
    data = user_or_repo(args.user_names)
    details = filter_data(data)
elif args.repo_names != None:
    # print('repo analysis')
    logger.info("repo analysis")
    data = user_or_repo(args.repo_names, 'repo')
    details = filter_data(data, 'repo')
else:
    # print('no specifications')
    logger.info("no specifications")
    data = user_or_repo(args.user_names) # just for now
    details = filter_data(data)

res = []

for i in details.keys():
    res.append([len(res)+1, i] + details[i])

for i in range(len(res)):
    for j in range(len(res[0])):
        res[i][j] = str(res[i][j])


# check output type
# return table, html, json or csv
x = PrettyTable()
if 'login' in details.keys():
    x.field_names = ["S.No.", "Arg"] + details['login']
else:
    x.field_names = ["S.No.", "Arg"] + details['full_name']
x.add_rows(res)
x.sortby = None
x.hrules = ALL

if args.out_type[0] == 'cmd':
    # print('output to cmd')
    logger.info("output to cmd")
    print(x)
elif args.out_type[0] == 'csv':
    # print('output to csv')
    logger.info("output to csv")
    create_csv(res)
elif args.out_type[0] == 'html':
    # print('output to html')
    logger.info("output to html")
    print(x.get_html_string())
elif args.out_type[0] == 'json':
    # print('output to json')
    logger.info("output to json")
    print(x.get_json_string())
