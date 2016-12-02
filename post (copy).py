def post(mydata):
    import urllib2
    import urllib
    #print mydata
    mydata2=urllib.urlencode(mydata)
    path='http://vetercek.com/postaje2/aladin/get.php'    
    req=urllib2.Request(path, mydata2)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    page=urllib2.urlopen(req).read()
    print page
