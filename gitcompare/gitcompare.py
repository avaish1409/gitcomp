import argparse
import logging


class GitCompare:
    api_base = 'https://api.github.com/'
    # explicitly request v3 of the API    https://docs.github.com/en/rest/overview/resources-in-the-rest-api#current
    # -version
    headers = {
        'Accept': 'application/vnd.github.v3+json'
    }
    logger: logging.Logger
    arg_parser: argparse.ArgumentParser

    def __init__(self):
        self.__init_logger()
        self.__init_arg_parser()

    def __init_logger(self):
        """
        initializes a logger instance with some defaults
        :return: None
        """
        logging.basicConfig(filename='newfile.log', format='%(asctime)s %(message)s', filemode='w')
        self.logger = logging.getLogger()

    def __init_arg_parser(self):
        """
        initializes an arg_parser with
        --user/-u
        --repo/-r
        --type/-o
        flags
        :return: None
        """
        self.arg_parser = argparse.ArgumentParser(description='Parses cmd line args for git-compare')
        self.arg_parser.add_argument("-u", "--user", type=str, nargs='*',
                                     metavar="user_name", default=None, dest='user_names',
                                     help="Opens and reads the specified text file.")

        self.arg_parser.add_argument("-r", "--repo", type=str, nargs='*',
                                     metavar="repo", default=None, dest='repo_names',
                                     help="Shows all the text files on specified directory path.\
                                        Type '.' for current directory.")

        self.arg_parser.add_argument("-o", "--type", type=str, nargs=1,
                                     metavar="output_dest", default=['cmd'], dest='out_type',
                                     help="Check whether the output should be printed in cmd, csv, html or json.\
                                        Type '.' for current directory.")
