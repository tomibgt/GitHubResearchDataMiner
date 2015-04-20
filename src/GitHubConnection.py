import sys
import time
import GitHubResearchDataMiner
import HelperFunctions
from github import Github
from github.GithubException import UnknownObjectException


class GitHubConnection(object):
    def __init__(self, user, repo):
        self.gitHubUserName = user
        self.gitHubRepoName = repo
        self.github = Github(GitHubResearchDataMiner.config.get('authentication', 'ghusername'), GitHubResearchDataMiner.config.get('authentication', 'ghpassword'))
        try: # Try to open the repository
            self.repo = self.github.get_repo(user+"/"+repo)
        except UnknownObjectException:
            print "Repository "+user+"/"+repo+" not found."
            GitHubResearchDataMiner.printHowToUse()
            sys.exit()
        self.requestRateTimer = HelperFunctions.millitimestamp()
        
    #This method is used to limit the rate of requests sent to GitHub
    def __choke(self):
        delta = float(HelperFunctions.millitimestamp()-self.requestRateTimer)
        if delta < 80:
            naptime=(80-delta)/1000
            if GitHubResearchDataMiner.config.get('debug', 'verbose'):
                print "Sleeping "+str(naptime)+" seconds..."
            time.sleep(naptime)
        self.requestRateTimer = HelperFunctions.millitimestamp()
        
    def getCommitMessages(self):
        self.__choke()
        commits = self.repo.get_commits()
        reva = ""
        for commit in commits:
            reva = reva + commit.commit.message+"\n"
        return reva
    
    '''
    Returns a handle to a csv file
    '''
    def getCsv(self):
        filepath = 'output.csv'
        fileh = open(filepath, 'w')
        fileh.write(self.getCsvHeaderRow())
        self.__choke()
        commits = self.repo.get_commits()
        for commit in commits:
            line = self.getCsvLineFromCommit(commit)
            if line != None:
                line = line+'\n'
                fileh.write(line.encode("utf-8"))
        fileh.close()
        return(filepath)

    '''
    Returns the header row for the output csv file
    '''
    def getCsvHeaderRow(self):
        return u"sha;commit date;committed file names;commit additions;commit deletions;commit changes;commit message"

    '''
    Parses the given GitHub commit into a row for the csv file.
    '''
    def getCsvLineFromCommit(self, commit):
        commitcommit  = commit.commit
        commitauthor  = commit.author
        commitfiles   = ""
        commitadds    = ""
        commitdels    = ""
        commitchanges = ""
        comma        = False
        try:
            for afile in commit.files:
                if(comma):
                    commitfiles   = commitfiles+','
                    commitadds    = commitadds+','
                    commitdels    = commitdels+','
                    commitchanges = commitchanges+','
                commitfiles   = commitfiles+afile.filename
                commitadds    = commitadds+str(afile.additions)
                commitdels    = commitdels+str(afile.deletions)
                commitchanges = commitchanges+str(afile.changes)
                comma = True
            if GitHubResearchDataMiner.config.get('debug', 'verbose'):
                print "Read commit "+commit.sha+": "+commitcommit.message+";"+str(commitauthor)
            reva = commit.sha+";"+str(commitauthor.created_at)+";"+commitfiles+";"+commitadds+";"+commitdels+";"+commitchanges+";"+commitcommit.message
            reva = reva.replace('\n', ' ')
        except AttributeError as detail:
            print "Attribute Error for sha("+commit.sha+")", detail
            return(None)
            #raise
            #AttributeErrors are ignored, because some commits have no committer, which causes these errors
            #This means that some of the commits are dropped off
        return reva
    