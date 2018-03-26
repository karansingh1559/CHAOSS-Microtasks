## MICROTASK 2

Produce a Python script that adds a new GitHub repository (git and GitHub issues / pull requests) to a given set of Mordred configuration 
files. Test it by adding at least two repositories (in two separate steps) to a GrimoireLab dashboard, producing screenshots of the
results.

### TASK SCRIPT

The script has 2 arguments: the first one is the full URL of the repository i.e https://github.com/coala/coala-bears as opposed to github.com/coala/coala-bears

The second argument is a list of [N] .cfg files

**HOW TO RUN**
* Run the following command:
    
   ```python3 m2.py repo_link file1.cfg file2.cfg ...```
      
   This will modify the .json files of the configuration files specified
      
* Start your ElasticSearch and Kibana instances

* Change the values of the 'sortinghat user' to the username of your of your MySql/MariaDB instance, 'sortinghat password' to its corresponding password and [add your github api token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) to the github section.

* Run the mordred command 

  ```mordred -c org_name.cfg```

* Open kibana to see dashboards (by default on [port 5601](https://localhost:5601/))
