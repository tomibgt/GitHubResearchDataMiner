import sys
import time
import GitHubResearchDataMiner
import HelperFunctions
from github import Github
from github.GithubException import UnknownObjectException
from github.GithubObject import NotSet


class GitHubConnection(object):
    def __init__(self, config):
        self.config = config
        self.gitHubUserName = config.user
        self.gitHubRepoName = config.repo
        self.github = Github(config.get('authentication', 'ghusername'), config.get('authentication', 'ghpassword'))
        try: # Try to open the repository
            self.repo = self.github.get_repo(config.user+"/"+config.repo)
        except UnknownObjectException:
            print "Repository "+config.user+"/"+config.repo+" not found."
            GitHubResearchDataMiner.printHowToUse()
            sys.exit()
        self.requestRateTimer = HelperFunctions.millitimestamp()
        
    #This method is used to limit the rate of requests sent to GitHub
    def __choke(self):
        if self.config.get('debug', 'verbose'):
            print "Sleep? rate_limiting:"+str(self.github.get_rate_limit().rate.remaining)+" resettime:"+str(self.github.get_rate_limit().rate.reset)+" currenttime:"+str(time.time())
        if self.github.get_rate_limit().rate.remaining<3:
            naptime = self.github.get_rate_limit().rate.reset-int(time.time())+5
            if self.config.get('debug', 'verbose'):
                print "Sleeping "+str(naptime)+" seconds..."
            time.sleep(naptime)

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
    def getCsv(self, filepath):
        fileh = open(filepath, 'w')
        fileh.write(self.getCsvHeaderRow()+'\n')
        self.__choke()
        commits = self.repo.get_commits()
        for commit in commits:
            line = self.getCsvLineFromCommit(commit)
            if line != None:
                line = line+'\n'
                fileh.write(line.encode("utf-8"))
        issues  = self.repo.get_issues("*", "all", "*", NotSet, "", "created", "asc", self.repo.created_at)
        for issue in issues:
            line = self.getCsvLineFromIssue(issue)
            if line != None:
                line = line+'\n'
                fileh.write(line.encode("utf-8"))
        fileh.close()
        return(filepath)

    '''
    Returns the header row for the output csv file
    '''
    def getCsvHeaderRow(self):
        return u"sha;commit/create date;committed file names;commit additions;commit deletions;commit changes;commit message;issue title;issue closed;issue labels"

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
        commitchangetotal = 0
        comma        = False
        self.__choke()
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
                commitchangetotal += afile.changes
                comma = True
            if self.config.get('debug', 'verbose'):
                try:
                    print "Read commit "+commit.sha+": "+commitcommit.message+";"+str(commitauthor)
                except UnicodeEncodeError:
                    print "--Unicode failure in printing commit metadata--"
            reva = commit.sha+";"+str(commit.date)+";"+commitfiles+";"+commitadds+";"+commitdels+";"+str(commitchangetotal)+";"+commitcommit.message
            reva = reva.replace('\n', ' ')
        except AttributeError as detail:
            print "Attribute Error for sha("+commit.sha+")", detail
            return(None)
            #raise
            #AttributeErrors are ignored, because some commits have no committer, which causes these errors
            #This means that some of the commits are dropped off
        return reva

    def getCsvLineFromIssue(self, issue):
        issuetitle   = issue.title
        issuecreated = issue.created_at
        issueclosed  = issue.closed_at
        issuelabels  = ""
        comma        = False
        for alabel in issue.labels:
            if(comma):
                issuelabels = issuelabels+','
            issuelabels = issuelabels+alabel.name
            comma = True
        if self.config.get('debug', 'verbose'):
            try:
                print "Read issue "+str(issue.id)+": "+issuetitle+";"+str(issuecreated)+";"+str(issueclosed)
            except UnicodeEncodeError:
                print "--Unicode failure in printing issue metadata"
        reva = ";"+str(issuecreated)+";;;;;;"+issuetitle+";"+str(issueclosed)+";"+issuelabels
        reva = reva.replace('\n', ' ')
        return reva
    