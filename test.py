from lxml import etree


f=open('logined.html','r',encoding="utf-8")
text=f.read()
html=etree.parse('logined.html',etree.HTMLParser())
result=html.xpath('')




