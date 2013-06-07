import os
import urllib2
import sgmllib


class MyParser(sgmllib.SGMLParser):
    def parse(self, s):
        self.feed(s)
        self.close()

    def __init__(self, verbose=0):
        sgmllib.SGMLParser.__init__(self, verbose)
        self.hyperlinks = []

    def start_a(self, attributes):
        tempHyperlink = ""
        tempDl = False
        for name, value in attributes:
            if name == "href":
                tempHyperlink = value
            if name == "dl":
                tempDl = True
            if (tempDl):
                self.hyperlinks.append(tempHyperlink)

    def getHyperlinks(self):
        return self.hyperlinks

if __name__ == '__main__':
    try:
        for i in [str(i) for i in range(1,2300)]:
            #print("http://it-ebooks.info/book/" + i)
            response = urllib2.urlopen("http://it-ebooks.info/book/" + "1")
            page_source = response.read()
            myparser = MyParser()
            myparser.parse(page_source)
    except Exception, e:
        print(e)