from .gitcomp_core import GitComp
from .ser_de import Writer
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
            ''')

    mutually_exclusive = parser.add_mutually_exclusive_group()

    mutually_exclusive.add_argument('-u', '--user', type=str, nargs='+',
                                    metavar='user_name', default=None, dest='user_names',
                                    help='''
                                         -u, --user <username...>
                                         The GitHub username(s) to query against.
                                         Multiple usernames can be queried at a time by providing a space separated
                                         argument list.
                                         ''')

    mutually_exclusive.add_argument('-r', '--repo', type=str, nargs='+',
                                    metavar='repo', default=None, dest='repo_names',
                                    help='''
                                         -r, --repo <repo>
                                         The public GitHub repository to query against where repo takes the form:
                                         <user/repo>
                                         Example: -r octocat/Spoon-Knife
                                         ''')

    parser.add_argument('-t', '--type', type=str, nargs=1, choices=['json', 'csv', 'ascii'],
                        metavar='output_t', default='ascii', dest='out_type',
                        help='''
                                         -t, --type <type>
                                         Default: ascii
                                         Choose the format of output. All output is dumped to STDOUT unless output file
                                         is specified using -o, --output flag.
                                         The types available are:
                                         json: Show the result as JSON
                                         csv: Format the output to csv
                                         ascii: Show the result as an ASCII table
                                         html: Show output as html
                                         ''')

    parser.add_argument('-o', '--output', type=str, nargs=1, metavar='out', dest='output_file',
                        help='''
                            -o, --output <out_file>
                            Output to out_file, defaults to STDOUT.
                        '''
                        )

    return parser


def main():
    propmap = {
        'users': 'user_data',
        'repos': 'repo_data'
    }
    arg_parser = __get_arg_parser()
    args = arg_parser.parse_args()
    g = GitComp(users=args.user_names, repos=args.repo_names)
    # TODO cleanup
    # start cleanup
    prop = None
    tp = None
    out = None
    if args.user_names is not None:
        prop = propmap['users']
    elif args.repo_names is not None:
        prop = propmap['repos']
    if args.out_type is not None:
        tp = args.out_type
    if args.output_file is not None:
        out = args.output_file[0]
    # end cleanup
    w = Writer(obj=g, tp=tp, out_file=out, prop=prop)
    w.write()


if __name__ == '__main__':
    main()
