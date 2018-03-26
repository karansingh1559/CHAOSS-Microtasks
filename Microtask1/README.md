## MICROTASK 1

Produce a Python script that produces configuration files for Mordred to analyze a complete GitHub organization, excluding
repositories that are forks from other GitHub repositories. Test it with at least two GitHub organizations, producing screenshots
of the resulting dashboard.

### TASK SCRIPT

The script has one positional argument i.e the name of the organisation, and an optional argument --json
which is set to false by default.

**HOW TO RUN**
* RUN THE SCRIPT
    * Run the following command if you need a projects.json to be created alongwith the configuration file
    
      ```python3 m1.py org_name --json=True```
      
      This will create 2 files- org_name.cfg and projects.json
      
    * If you already have a projects.json file, run the following command:
    
      ```python3 m1.py org_name```
        
      This will create 1 file - org_name.cfg
* Start your ElasticSearch and Kibana instances

* Change the values of the 'sortinghat user' to the username of your of your MySql/MariaDB instance, 'sortinghat password' to its corresponding password and [add your github api token](https://help.github.com/articles/creating-a-personal-access-token-for-the-command-line/) to the github section.

* Run the mordred command 

  ```mordred -c org_name.cfg```

* Open kibana to see dashboards (by default on [port 5601](https://localhost:5601/))
