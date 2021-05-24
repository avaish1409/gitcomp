from .gitcomp_core import GitComp
from .user import User
from .repository import Repository
from .ser_de import to_json_str, to_dict
import argparse

__all__ = [
    'GitComp',
    'User',
    'Repository',
    'to_dict',
    'to_json_str'
]


def __get_arg_parser() -> argparse.ArgumentParser:
    """
            initializes an arg_parser with
            --user/-u
            --repo/-r
            --type/-o
            flags
            :return: argparse.ArgumentParser
            """
    parser = argparse.ArgumentParser(description='''
            gitcomp
            A CLI utility to compare the vital stats of GitHub repositories
            ''')

    parser.add_argument('-u', '--user', type=str, nargs='+',
                        metavar='user_name', default=None, dest='user_names',
                        help='''
                                         -u, --user <username...>
                                         The GitHub username(s) to query against.
                                         Multiple usernames can be queried at a time by providing a space separated
                                         argument list.
                                         ''')

    parser.add_argument('-r', '--repo', type=str, nargs='+',
                        metavar='repo', default=None, dest='repo_names',
                        help='''
                                         -r, --repo <repo>
                                         The public GitHub repository to query against where repo takes the form:
                                         <user/repo>
                                         Example: -r octocat/Spoon-Knife
                                         ''')

    parser.add_argument('-t', '--type', type=str, nargs=1,
                        metavar='output_dest', default=['cmd'], dest='out_type',
                        help='''
                                         -t, --type <type>
                                         Default: cmd
                                         Choose the format of output. All output is dumped to STDOUT
                                         The types available are:
                                         cmd: Show the result as an ASCII table
                                         csv: Format the output to csv
                                         html: Show output as html
                                         json: Show the result as JSON
                                         ''')

    return parser


def main():
    arg_parser = __get_arg_parser()
    args = arg_parser.parse_args()
    if args.user_names is not None or args.repo_names is not None:
        g = GitComp(users=args.user_names, repos=args.repo_names, display_type=args.out_type[0])
        print(g.get_table())


if __name__ == '__main__':
    main()
