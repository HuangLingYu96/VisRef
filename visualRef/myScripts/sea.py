class seaNode:
    # 构造器
    def __init__(self, doi):
        self.tdoi = doi
        self.ttitle = 'Unknown'
        self.tjournal = 'Unknown'
        self.ttime = 'Unknown'
        self.tyear='Unknown'
        self.ttype = 'Unknown'
        self.tvolume='Unknown',
        self.tissue='Unknown',
        self.page_from='Unknown',
        self.page_to='Unknown',
        self.tauthors = 'Unknown'
        self.tlink = r'https://doi.org/' + doi

    def getDoi(self):
        return self.tdoi

    def getLink(self):
        return self.tlink

    # 标题
    def setTitle(self, ttitle):
        self.ttitle=ttitle
    def getTitle(self):
        return self.ttitle

    #journal
    def setJournal(self,tjournal):
        self.tjournal=tjournal
    def getJournal(self):
        return self.tjournal

    #year
    def setYear(self,tyear):
        self.tyear=tyear
    def getYear(self):
        return self.tyear

    #time
    def setTime(self,ttime):
        self.ttime=ttime
    def getTime(self):
        return self.ttime

    #type
    def setType(self,ttype):
        self.ttype=ttype
    def getType(self):
        return self.ttype

    #volume
    def setVolume(self,tvolume):
        self.tvolume=tvolume
    def getVolume(self):
        return self.tvolume

    #issue
    def setIssue(self,tissue):
        self.tissue=tissue
    def getIssue(self):
        return self.tissue

    #page_from
    def setPageFrom(self,page_from):
        self.page_from=page_from
    def getPageFrom(self):
        return self.page_from

    #page_to
    def setPageTo(self,page_to):
        self.page_to=page_to
    def getPageTo(self):
        return self.page_to

    #authors
    def setAuthors(self,tauthors):
        self.tauthors=tauthors
    def getAuthors(self):
        return self.tauthors