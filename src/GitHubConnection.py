import datetime
import time
import GitHubResearchDataMiner
from github import Github


class GitHubConnection(object):
    def __init__(self, user, repo):
        self.gitHubUserName = user
        self.gitHubRepoName = repo
        self.github = Github(GitHubResearchDataMiner.config.get('authentication', 'ghusername'), GitHubResearchDataMiner.config.get('authentication', 'ghpassword'))
        self.repo = self.github.get_repo(user+"/"+repo)
        self.requestRateTimer = datetime.datetime.now().microsecond
        
    #This method is used to limit the rate of requests sent to GitHub
    def __choke(self):
        delta = datetime.datetime.now().microsecond-self.requestRateTimer
        if delta < 80000:
            time.sleep(delta/1000000)
        self.requestRateTimer = datetime.datetime.now().microsecond
        
    def getCommitMessages(self):
        self.__choke()
        commits = self.repo.get_commits()
        reva = ""
        for commit in commits:
            reva = reva + commit.commit.message+"\n"
        return reva
    
    #Returns a handle to a csv file
    def getCsv(self):
        filepath = 'output.csv'
        fileh = open(filepath, 'w')
        self.__choke()
        commits = self.repo.get_commits()
        for commit in commits:
            fileh.write(self.getCsvLineFromCommit(commit)+'\n')
        fileh.close()
        return(filepath)
        
    def getCsvLineFromCommit(self, commit):
        commitcommit = commit.commit
        commitfiles  =  ""
        comma        = False
        for afile in commit.files:
            commitfiles = commitfiles+afile.filename
            if(comma):
                commitfiles = commitfiles+','
            comma = True
        reva = commit.sha+";"+commitfiles+";"+commitcommit.message
        #reva = commit.sha+";"+commitfile.additions+";"+commitfile.blob_url+";"+commitfile.changes+";"+commitfile.contents_url+";"+commitfile.deletions+";"+commitfile.filename+";"+commitfile.patch+";"+commitfile.raw_url+";"+commitfile.status+";"+commitcommit.message
        reva = reva.replace('\n', ' ')
        return reva
    