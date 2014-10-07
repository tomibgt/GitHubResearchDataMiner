class GitHubConnection(object):
    def __init__(self, user, repo):
        self.gitHubUser = user
        self.gitHubRepo = repo
        
    def getCommits(self):
        return ""