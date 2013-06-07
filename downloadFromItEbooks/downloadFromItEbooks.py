#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import urllib
import urllib2
import sgmllib
from mechanize import Browser
from mega import Mega


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
        mega = Mega()
        m = mega.login("mail", "password")
        for i in [str(i) for i in range(1,2300)]:
            print("http://it-ebooks.info/book/" + i)

            #On récupère le titre du livre
            br = Browser()
            br.open("http://it-ebooks.info/book/" + i)
            file_title = br.title().split(" - ")[0]

            #On récupère le lien de téléchargement
            response = urllib2.urlopen("http://it-ebooks.info/book/" + i)
            page_source = response.read()
            myparser = MyParser()
            myparser.parse(page_source)

            #On effectue le téléchargement
            print("Téléchargement du livre : " + file_title)
            urllib.urlretrieve ("http://it-ebooks.info" + myparser.getHyperlinks()[0], 
                                file_title + ".pdf")

            #Upload chez Mega
            file = m.upload(file_title + ".pdf",
                            m.find("Books"))
            print("Uploaded : " + file_title + ".pdf" + " Link : " + m.get_upload_link(file))

            #On supprime le fichier local du serveur
            os.remove(file_title + ".pdf")
            print("Deleted : " + file_title + ".pdf")
    except Exception, e:
        print(e)