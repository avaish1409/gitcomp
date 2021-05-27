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
                                         -u, --user <username...>\n
                                         The GitHub username(s) to query against.\n
                                         Multiple usernames can be queried at a time by providing a space separated
                                         argument list.\n
                                         ''')

    mutually_exclusive.add_argument('-r', '--repo', type=str, nargs='+',
                                    metavar='repo', default=None, dest='repo_names',
                                    help='''
                                         -r, --repo <repo>\n
                                         The public GitHub repository to query against where repo takes the form:\n
                                         <user/repo>.\n
                                         Example: -r octocat/Spoon-Knife\n
                                         ''')

    parser.add_argument('-t', '--type', type=str, nargs=1, choices=['json', 'csv', 'ascii', 'html'],
                        metavar='output_t', default=['ascii'], dest='out_type',
                        help='''
                                         -t, --type <type>\n
                                         Default: ascii\n
                                         Choose the format of output. All output is dumped to STDOUT unless output file
                                         is specified using -o, --output flag.\n
                                         The types available are:\n
                                         json: Show the result as JSON.\n
                                         csv: Show the output as csv.\n
                                         ascii: Show the result as an ASCII table.\n
                                         html: Show output as HTML table.\n
                                         ''')

    parser.add_argument('-o', '--output', type=str, nargs=1, metavar='out', dest='output_file',
                        help='''
                            -o, --output <out_file>\n
                            Output to out_file, defaults to STDOUT.\n
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
        tp = args.out_type[0]
    if args.output_file is not None:
        out = args.output_file[0]
    # end cleanup
    w = Writer(obj=g, tp=tp, out_file=out, prop=prop)
    w.write()


if __name__ == '__main__':
    main()
