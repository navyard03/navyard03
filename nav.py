import pandas as pd
import requests
import configparser
import csv
import sys
import os
import gitlab

class metrics:

  def __init__(self) -> None:
    #Disabling warnings
    requests.packages.urllib3.disable_warnings()
    config = configparser.RawConfigParser()
    path_current_directory = os.path.dirname(__file__)
    path_config_file = os.path.join(path_current_directory, '.config')
    print("config file is" + str(path_config_file))
    config = configparser.ConfigParser()
    config.read(path_config_file)
    # Retrieving values 
    print("1111")
#    self.urlcomp = config.get('gitURL')
    self.urlcomp = '###'
    print("222")
    #privateToken = config.get('privateToken')
    privateToken = '###'
    if privateToken == '':
        raise ValueError("please add private token")
    self.headers = {'PRIVATE-TOKEN': privateToken}
    print("navaaaa")
   # fileName = "csv_file"
   # self.csv_file = open(fileName, "w")
   # self.csv_file.write("Project ID" + "," + "Project Name" + "," + "languages" +  "\n")
   
  def getAllProjects(self):
       projects = []
       pageNum = 6
       projectsURL = self.urlcomp + '/projects?per_page=100&page=' + str(pageNum)
       rcomp = requests.get(projectsURL, headers=self.headers,verify=False)
       if rcomp.status_code != 200:
           err_proj = {'status_code': rcomp.status_code, 'message': rcomp.reason}
           print("Something we wrong!, no projects to display")
           print(err_proj)
           exit()
       projects_df = pd.DataFrame.from_dict(rcomp.json())
       currentPage = int(rcomp.headers["X-Page"])
       totalPages = int(rcomp.headers["X-Total-Pages"])

       print("Total # of projects from Header -->" + rcomp.headers["X-Total"])
       print("Current Page -->" + str(currentPage) + ": Total Number of Pages -->" + str(totalPages))

       print("currentpage")
       print(currentPage)
       while currentPage == pageNum : 
             print("pageeeeeeeeee")
             print(pageNum)
             projectURL = self.urlcomp + '/projects?per_page=100&page=' + str(pageNum)
             rcomp = requests.get(projectsURL, headers=self.headers,verify=False)
             if rcomp.status_code != 200:
                  err_proj = {'status_code': rcomp.status_code, 'message': rcomp.reason}
                  print(err_proj)
                  #currentPage +=1
                  continue
             projects_df_temp = pd.DataFrame.from_dict(rcomp.json())
        
             frames = [projects_df,projects_df_temp]
             projects_df = pd.concat(frames)

             currentPage = int(rcomp.headers["X-Page"])
             totalPages = int(rcomp.headers["X-Total-Pages"])

             print("current page -->" + str(currentPage) + ": Totalno. of pages -->" + str(totalPages))

             if 'id' in projects_df.columns:
               projects = projects_df[['id', 'name']].set_index('id').to_dict()['name']
               print("Total # of projects -->" + str(len(projects)))
             return projects


  def getdetails(self,project_id):
      details = []
      detailsByProjectUrl = self.urlcomp + "projects/" + str(project_id) + "/languages"
      rcomp = requests.get(detailsByProjectUrl, headers=self.headers,verify=False)
      print(rcomp.json())
      if rcomp.status_code != 200:
         err_details = {'Projects': str(project_id), 'status_code': rcomp.status_code, 'message': rcomp.reason}
         return err_details
      else:
         details = rcomp.json()
         print("aaaaaaaaaa")
         print(details)
      return details


if __name__ == "__main__":
     metrics = metrics()
     visited_project_ids = []
     #groups = metrics.getgroups()
     #for group_id, group_name in groups.items():
     projects = metrics.getAllProjects()
     fileName = "list.csv"
     csv_file = open(fileName, "a")
     csv_file.write("Project ID" + "," + "Project Name" + "," + "languages" +  "\n")
     if "status_code" in projects :
             print("Erros fetching project: ",projects)
     else:
             for project_id, project_name in projects.items():
                 if project_id not in visited_project_ids:
                     details = metrics.getdetails(project_id)
                     print("111-details")
                     print(details)
                     print("222-projectid")
                     print(str(project_id))
                     print("333-projectname")
                     print(project_name)
                     if "status_code" in details:
                         print("Error fetching detail: ")
                     else:
#                         fileName = "list.csv"
 #                        csv_file = open(fileName, "a")
                         #csv_file.write("Project ID" + "," + "Project Name" + "," + "languages" +  "\n")
                         csv_file.write(str(project_id) + "," + project_name + "," + str(details) + "\n")
                     visited_project_ids.append(project_id)
csv_file.close()  
