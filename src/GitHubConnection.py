from github import Github

class GitHubConnection(object):
    def __init__(self, user, repo):
        self.gitHubUserName = user
        self.gitHubRepoName = repo
        self.github = Github()
        #self.repo = self.github.get_repo(self.gitHubUserName+"/"+self.gitHubRepoName)
        self.repo = self.github.get_repo(user+"/"+repo)
        
    def getCommits(self):
        commits = self.repo.get_commits()
        reva = ""
        for commit in commits:
            reva = reva + commit.commit.message+"\n"
        return reva