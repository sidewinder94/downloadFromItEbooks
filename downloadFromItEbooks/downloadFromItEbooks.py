#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import os
import urllib
import urllib2
import sgmllib
from mechanize import Browser


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
            if value == "dl":
                tempDl = True
            if (tempDl):
                if (tempHyperlink != ""):
                    self.hyperlinks.append(tempHyperlink)
                    tempDl = False

    def getHyperlinks(self):
        return self.hyperlinks

if __name__ == '__main__':
    try:
        for i in [str(i) for i in range(1,2300)]:
            #print("http://it-ebooks.info/book/" + i)

            #On récupère le titre du livre
            br = Browser()
            br.open("http://it-ebooks.info/book/" + "1")
            file_title = br.title().split(" - ")[0]

            #On récupère le lien de téléchargement
            response = urllib2.urlopen("http://it-ebooks.info/book/" + "1")
            page_source = response.read()
            myparser = MyParser()
            myparser.parse(page_source)

            #On effectue le téléchargement
            print("Téléchargement du livre : %S", file_title)
            urllib.urlretrieve (myparser.getHyperlinks[0], file_title + ".pdf")
    except Exception, e:
        print(e)