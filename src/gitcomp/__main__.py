from .gitcomp_core import GitComp
from .ser_de import Writer, PROP
import argparse


def __get_arg_parser() -> argparse.ArgumentParser:
    """
            initializes an arg_parser with
            --user/-u
            --repo/-r
            --type/-t
            flags
            :return: argparse.ArgumentParser
            """
    parser = argparse.ArgumentParser(description='''
            gitcomp
            A CLI utility to compare the vital stats of GitHub repositories
            ''', formatter_class=argparse.RawTextHelpFormatter)

    mutually_exclusive = parser.add_mutually_exclusive_group()

    mutually_exclusive.add_argument('-u', '--user', type=str, nargs='+',
                                    metavar='user_name', default=[], dest='user_names',
                                    help='''
                                         -u, --user <username...>
                                         The GitHub username(s) to query against.
                                         Multiple usernames can be queried at a time by providing a space separated
                                         argument list.
                                         ''')

    mutually_exclusive.add_argument('-r', '--repo', type=str, nargs='+',
                                    metavar='repo', default=[], dest='repo_names',
                                    help='''
                                         -r, --repo <repo>
                                         The public GitHub repository to query against where repo takes the form:
                                         <user/repo>.
                                         Example: -r octocat/Spoon-Knife
                                         ''')

    parser.add_argument('-t', '--type', type=str, nargs=1, choices=['json', 'csv', 'ascii', 'html'],
                        metavar='output_t', default=['ascii'], dest='out_type',
                        help='''
                                         -t, --type <type>
                                         Default: ascii
                                         Choose the format of output. All output is dumped to STDOUT unless output file
                                         is specified using -o, --output flag.
                                         The types available are:
                                         json: Show the result as JSON.
                                         csv: Show the output as csv.
                                         ascii: Show the result as an ASCII table.
                                         html: Show output as HTML table.
                                         ''')

    parser.add_argument('-o', '--output', type=str, nargs=1, default=[None], metavar='out', dest='output_file',
                        help='''
                            -o, --output <out_file>
                            Output to out_file, defaults to STDOUT.
                        ''')

    return parser


def safe_exit(parser: argparse.ArgumentParser):
    parser.print_help()
    exit(2)


def main():
    arg_parser = __get_arg_parser()
    args = arg_parser.parse_args()
    if len(args.user_names) == len(args.repo_names) == 0:
        safe_exit(arg_parser)
    users = list(set(args.user_names)) or None
    repos = list((set(args.repo_names))) or None
    g = GitComp(users=users, repos=repos)
    prop = None
    if users is not None:
        prop = PROP['users'].value
    elif repos is not None:
        prop = PROP['repos'].value
    out_type = args.out_type[0]
    out_file = args.output_file[0]
    Writer(obj=g, out_type=out_type, out_file=out_file, prop=prop).write()


if __name__ == '__main__':
    main()
