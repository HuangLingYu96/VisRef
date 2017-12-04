class refNode:
    #构造器
    def __init__(self,doi,category):
        self.doi=doi
        self.category=category
        self.title='Unknown'
        self.publisher='Unknown'
        self.date='Unknown'
        self.citation='Unknown'
        self.author='Unknown'
        self.link=r'https://doi.org/'+doi
        self.subject='Unknown'

    def getDoi(self):
        return self.doi

    def getCategory(self):
        return self.category

    #标题
    def setTitle(self,title):
        self.title=title
    def getTitle(self):
        return self.title

    #杂志
    def setPublisher(self,publisher):
        self.publisher=publisher
    def getPublisher(self):
        return self.publisher

    #日期
    def setDate(self,date):
        self.date=date
    def getDate(self):
        return self.date

    #被引用次数
    def setCitation(self,citation):
        self.citation=citation
    def getCitation(self):
        return self.citation

    #作者
    def setAuthor(self,author):
        self.author=author
    def getAuthor(self):
        return self.author

    def getLink(self):
        return self.link

    #主题
    def setSubject(self,subject):
        self.subject=subject
    def getSubject(self):
        return self.subject