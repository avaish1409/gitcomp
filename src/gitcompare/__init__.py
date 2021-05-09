import argparse
import urllib.request
import json
from prettytable import PrettyTable, ALL
import logging


# TODO add function descriptions

def user_or_repo(arr, option='user'):
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


def all_repo():
    # repo list
    # return list of all repo details
    pass


# keep only required user/repo details for comparison
def filter_data(raw_data, option='user'):
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


def create_csv(arr):
    for i in arr:
        print(', '.join(i))
    return


def init_logger():
    logging.basicConfig(filename='newfile.log', format='%(asctime)s %(message)s', filemode='w')
    return logging.getLogger()


def init_parser():
    parser = argparse.ArgumentParser(description='Parses cmd line args for git-compare')
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
    return parser


def main():
    logger = init_logger()
    arg_parser = init_parser()
    args = arg_parser.parse_args()
    if args.user_names is not None:
        logger.info("user analysis")
        data = user_or_repo(args.user_names)
        details = filter_data(data)
    elif args.repo_names is not None:
        logger.info("repo analysis")
        data = user_or_repo(args.repo_names, 'repo')
        details = filter_data(data, 'repo')
    else:
        logger.info("no specifications")
        data = user_or_repo(args.user_names)  # just for now
        details = filter_data(data)

    res = []

    for i in details.keys():
        res.append([len(res) + 1, i] + details[i])

    for i in range(len(res)):
        for j in range(len(res[0])):
            res[i][j] = str(res[i][j])

    x = PrettyTable()
    if 'login' in details.keys():
        x.field_names = ["S.No.", "Arg"] + details['login']
    else:
        x.field_names = ["S.No.", "Arg"] + details['full_name']
    x.add_rows(res)
    x.sortby = None
    x.hrules = ALL

    if args.out_type[0] == 'cmd':
        logger.info("output to cmd")
        print(x)
    elif args.out_type[0] == 'csv':
        logger.info("output to csv")
        create_csv(res)
    elif args.out_type[0] == 'html':
        logger.info("output to html")
        print(x.get_html_string())
    elif args.out_type[0] == 'json':
        logger.info("output to json")
        print(x.get_json_string())


if __name__ == '__main__':
    main()