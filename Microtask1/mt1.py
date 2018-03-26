'''
Script to produce configuration file for an organization
to analyze a github repo, excluding repositories that are
forked from other repositories
'''

import sys
import argparse
import requests
import json
import configparser

def create_config(org_name):
    '''
    function to create config file
    :params org_name : name of organisation to be analyzed
    '''

    config = configparser.ConfigParser()

    config.add_section('general')
    config.set('general', 'short_name', org_name)
    config.set('general', 'update', 'false')
    config.set('general', 'sleep', '0')
    config.set('general', 'debug', 'true')
    config.set('general', 'min_update_delay', '10')
    config.set('general', 'logs_dir', '/tmp/logs')
    config.set('general', 'kibana', '"5"')

    config.add_section('projects')
    config.set('projects', 'projects_file', 'projects.json')

    config.add_section('es_collection')
    config.set('es_collection', 'url', 'http://localhost:9200')
    config.set('es_collection', 'user', '')
    config.set('es_collection', 'password', '')

    config.add_section('es_enrichment')
    config.set('es_enrichment', 'url', 'http://127.0.0.1:9200')
    config.set('es_enrichment', 'user', '')
    config.set('es_enrichment', 'password', '')
    config.set('es_enrichment', 'autorefresh', 'false')

    config.add_section('sortinghat')
    config.set('sortinghat', 'host', 'localhost')
    config.set('sortinghat', 'user', 'karan')
    config.set('sortinghat', 'password', 'password')
    config.set('sortinghat', 'database', 'mysql')
    config.set('sortinghat', 'load_orgs', 'false')
    config.set('sortinghat', 'unify_method', '')
    config.set('sortinghat', 'unaffiliated_group', 'Unknown')
    config.set('sortinghat', 'affiliate', 'True')
    config.set('sortinghat', 'autoprofile', '[customer,git,github]')
    config.set('sortinghat', 'matching', '[email]')
    config.set('sortinghat', 'sleep_for', '0')
    config.set('sortinghat', 'bots_names', '[Beloved Bot]')

    config.add_section('panels')
    config.set('panels', 'kibiter_time_from', '"now-90d"')

    config.add_section('phases')
    config.set('phases', 'collection', 'true')
    config.set('phases', 'identities', 'true')
    config.set('phases', 'enrichment', 'true')
    config.set('phases', 'panels', 'true')
    
    config.add_section('github')
    config.set('github', 'raw_index', 'github_test-raw')
    config.set('github', 'enriched_index', 'github_test')
    config.set('github', 'api-token', '360b4c3b27d3a2e074c467d07380628e1db9677a')
    config.set('github', 'sleep-for-rate', 'true')

    with open(org_name + ".cfg", "w") as conf:
        config.write(conf)

def create_json(org_name):
    '''
    function to create json file for the
    organisation passed in the argument
    :params org_name: name of the organisation
    '''

    org_url = "https://api.github.com/users/" + org_name + "/repos"
    gitList = []
    githubList = []
    r = requests.get(org_url + "?page=0")

    '''loop that checks if the repository list has more pages''' 
    while ('next' in r.links or not r.links):
        for repo in r.json():
            if not repo['fork']:
                gitList.append(repo['clone_url'])
                githubList.append(repo['html_url'])
        if not r.links:
            break
        r = requests.get(r.links['next']['url'])

    '''dump the data to a json file after fetching the list'''
    jsonFile = {}
    jsonFile[org_name] = {}
    jsonFile[org_name]['git'] = gitList
    jsonFile[org_name]['github'] = githubList
    with open(org_name + ".json", "w") as jsonf:
        json.dump(jsonFile, jsonf, indent=4)

def parse_args():
    '''
    function to parse the arguments passed on the command line
    '''

    parser = argparse.ArgumentParser(description='analyze a github repo')

    parser.add_argument('org', nargs='?', help = 'name of the organisation', default='chaoss')
    parser.add_argument('--json', dest='json', help='flag to specify if a json file is to be created', nargs='?', default='False', const='False')
    args = parser.parse_args()

    return args

def main():
    if len(sys.argv) < 2:
        err= 'The script must be run with atleast one argument\n'
        sys.stderr.write(err)
        sys.exit(1)
    args = parse_args()

    org_name=''
    for e in str(args.org):
        if e.isalpha():
            org_name+=e
    #org_name=args.org[1:-1]

    if args.json=='True':
        create_json(org_name)
    create_config(org_name)

if __name__ == '__main__':
    try:
         main()
    except RuntimeError as e:
        err = 'Error: %s\n' % str(e)
        sys.stderr.write(err)
        sys.exit(1)
