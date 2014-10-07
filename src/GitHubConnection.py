from github import Github

class GitHubConnection(object):
    def __init__(self, user, repo):
        self.gitHubUser = user
        self.gitHubRepo = repo
        self.github = Github()
        
    def getCommits(self):
        return ""