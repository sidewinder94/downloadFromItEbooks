import os
import urllib2
from elementtree.ElementTree import ElementTree


if __name__ == '__main__':
    try:
        for i in [str(i) for i in range(1,2300)]:
            #print("http://it-ebooks.info/book/" + i)
            response = urllib2.urlopen("http://it-ebooks.info/book/" + i)
    except Exception, e:
        print(e)