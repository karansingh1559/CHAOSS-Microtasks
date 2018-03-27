import os
import json
import configparser
import elasticsearch.Elasticsearch
import elasticsearch_dsl.Search

client = Elasticsearch()
FOLDER_PATH = './'


def delete_repo(to_delete):
	#deletes the repository(github issues and git commits) from the dashboard by deleting the 
	#elasticsearch data.
	#:param to_delete : the url of the repository to be deleted
	print("Repository" , to_delete, "will be deleted")
	s = Search(using = es, index = "git_test", doc_type="items").\
		query("match", origin=to_delete + ".git")
		
	response = s.delete()

	s = Search(using = es, index = "git_test-raw", doc_type="items").\
		query("match", origin=to_delete + ".git")
		
	response = s.delete()
	
	s = Search(using = es, index = "github_test", doc_type="items").\
		query("match", origin=to_delete )
	response = s.delete()
	

	s = Search(using = es, index = "github_test-raw", doc_type="items").\
		query("match", origin=to_delete )
	response = s.delete()

def list_repos(gh_index):
    """
    Lists the repositories part of the current index
    :params gh_index: index to list repositories from
    """

    print("The current index has the following repositories:")
    s = client.search(index=gh_index)
    s.aggs.bucket('repos','terms', field='origin')
    response = s.execute()
    repoList = response['aggregations']['repos']['buckets']
    print(repoList)
    for i,res in enumerate(repoList, start=1):
        print(i, res['key'])
    
    print("Type the serial number of the repository to be deleted")
    num = int(input())
    return repoList[num-1]['key']

def main():
    '''print indexed list of .cfg files in FOLDER_PATH'''
    cfg_files=[]
    files=os.listdir(FOLDER_PATH)
    for f in files:
        if f.endswith('.cfg'):
            cfg_files.append(f)
    for index, cfg in enumerate(cfg_files, start=1):
         print(index, cfg)
    
    '''obtain the index to work on'''
    print("Type the serial number of the configuration file to get the index from")
    num = int(input())
    if not num <=len(cfg_files) or not num >0:
        return
    config=configparser.ConfigParser()
    config.read(cfg_files[num-1])
    gh_index=config['github']['enriched_index']

    targetRepo = list_repos(gh_index)
    delete_repo(to_delete)
    

if __name__ == '__main__':
    try:
        main()
    except RuntimeError as e:
        err = 'Error: %s\n' % str(e)
        sys.stderr.write(err)
        sys.exit(1)
