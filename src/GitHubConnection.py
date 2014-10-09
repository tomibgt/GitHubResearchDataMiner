from github import Github

class GitHubConnection(object):
    def __init__(self, user, repo):
        self.gitHubUserName = user
        self.gitHubRepoName = repo
        self.github = Github()
        #self.repo = self.github.get_repo(self.gitHubUserName+"/"+self.gitHubRepoName)
        self.repo = self.github.get_repo(user+"/"+repo)
        
    def getCommitMessages(self):
        commits = self.repo.get_commits()
        reva = ""
        for commit in commits:
            reva = reva + commit.commit.message+"\n"
        return reva
    
    #Returns a handle to a csv file
    def getCsv(self):
        filepath = 'output.csv'
        fileh = open(filepath, 'w')
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
    