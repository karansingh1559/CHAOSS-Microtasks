'''
Script that takes in the link of a github repository 
and adds to a specified list of cfg files
'''

import sys
import argparse
import os.path
import configparser
import json

def parse_args():
    '''
    function to parse command line arguments
    '''
    parser = argparse.ArgumentParser(description='Add repo to list of cfg files')
    parser.add_argument('repo_link', help='github repo link')
    parser.add_argument('cfg_files', nargs='+', help = 'list of cfg files')
    args = parser.parse_args()
    return args

def check_link(repo_link):
    if not (repo_link).startswith('https://') or not (repo_link).endswith('.git'):
        print('Please re-run the script with a valid repo link')
        sys.exit(1)

def check_cfg(cfg_files):
    for arg in cfg_files:
        if not arg.endswith('.cfg'):
            print('Please re-run the script with .cfg files')
            sys.exit(1)
        elif not os.path.isfile(arg):
            print('File {0} does not exist'.format(str(arg)))
            sys.exit(1)

def append_repo(cfg_files):
    for arg in args.cfg_files:
        config = configparser.ConfigParser()
        config.read(arg)
        jsonFile=config['projects']['projects_file']

        with open(jsonFile) as jsonf:
            d=json.load(jsonf)
            gitList=d[repo_org]['git']
            githubList=d[repo_org]['github']
            gitList.append(args.repo_link + '.git')
            githubList.append(args.repo_link)
            d[repo_org]['git']=gitList
            d[repo_org]['github']=githubList

        with open(jsonFile, 'w') as f:	
            json.dump(d, f, indent=4)

def main():
    if len(sys.argv) < 2:
        err= 'The script must be run with atleast one argument\n'
        sys.stderr.write(err)
        sys.exit(1)
    args = parse_args()

    '''check for valid repo link'''
    check_link(args.repo_link)

    '''check for valid cfg files'''
    check_cfg(args.cfg_files)

    '''extract organisation name'''
    url_parts=(args.repo_link).split('/')
    repo_org=url_parts[3]

    '''add repository to the json file of each cfg file'''
    append_repo(args.cfg_files)

if __name__ == '__main__':
    try:
        main()
    except RuntimeError as e:
        err = 'Error: %s\n' % str(e)
        sys.stderr.write(err)
        sys.exit(1)

