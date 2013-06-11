#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import urllib
import urllib2
import sgmllib
import sys
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

def megaUpload(userName, password, fileName, destination, error=0):
    if error <> 0:
        print "Upload try n°" + str(error)
        print "Failed will try again in " + str(error*5) + " seconds"
    try:
        #Si on en est pas au premier essai on att 5 sec * le nombre d'essais
        time.sleep(5*error)
        mega = Mega()
        m = mega.login(userName, password)
        file = m.upload(fileName, m.find(destination)[0])
        return m.get_upload_link(file)
    except Exception, e:
        mega = Mega()
        m = mega.login(userName, password)
        file = m.find(fileName)
        if (file <> None):
            return m.get_upload_link(file)
        else:
            print "error : " , e
            megaUpload(userName, password, fileName, destination, error+1)

if __name__ == '__main__':
    user = sys.argv[1]
    password = sys.argv[2] 
    start = sys.argv[3]
    try:
        start = int(start)
    except:
        start = 1
    for i in range(start,2300):
        try:
            print("http://it-ebooks.info/book/" + str(i))

            #On récupère le titre du livre
            br = Browser()
            br.open("http://it-ebooks.info/book/" + str(i))
            file_title = br.title().split(" - ")[0]

            #On récupère le lien de téléchargement
            response = urllib2.urlopen("http://it-ebooks.info/book/" + str(i))
            page_source = response.read()
            myparser = MyParser()
            myparser.parse(page_source)

            #On effectue le téléchargement
            print("Téléchargement du livre : " + file_title)
            #urllib.urlretrieve ("http://it-ebooks.info" + myparser.getHyperlinks()[0], 
            #                    file_title + ".pdf")

            url = "http://it-ebooks.info" + myparser.getHyperlinks()[0]

            file_name = file_title + ".pdf"
            u = urllib2.urlopen(url)
            f = open(file_name, 'wb')
            meta = u.info()
            file_size = int(meta.getheaders("Content-Length")[0])
            print "Downloading: %s Bytes: %s" % (file_name, file_size)

            file_size_dl = 0
            block_sz = 8192
            while True:
                buffer = u.read(block_sz)
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8)*(len(status)+1)
                print status,

            f.close()

            #Upload chez Mega
            
            print("Uploaded : " + file_title + ".pdf" + " Link : " + 
                  megaUpload(user,password,file_title + ".pdf","Books"))

            #On supprime le fichier local du serveur
            os.remove(file_title + ".pdf")
            print("Deleted : " + file_title + ".pdf")
        except Exception, e:
            print(e)