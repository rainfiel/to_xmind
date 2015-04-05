# -*- coding: utf-8 -*-

import os,sys,time
import xmltodict as xml2dict
import collections
import codecs
import string, random
import zipfile


def id_generator(size=26, chars=string.ascii_lowercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def loadXML(path):
	f = codecs.open(path, 'r', 'utf-8')
	c = f.read()
	f.close()

	return xml2dict.parse(c)

def writeXML(data, path):
	txt=xml2dict.unparse(data)
	f = codecs.open(path, 'w', 'utf-8')
	f.write(txt)
	f.close()

def topicInfo(topic):
	topic['@timestamp'] = str(int(time.time()*1000))
	topic['@id'] = id_generator()

def handleOutline(root, src):
	t = type(root)
	if t == collections.OrderedDict:
		node = collections.OrderedDict()
		node['title'] = root['@text']
		note = root.get('@_note',None)
		if note:
			node['notes'] = collections.OrderedDict({'html':collections.OrderedDict({'xhtml:p':note}), 'plain':note})

		children = root.get('outline', None)
		if children:
			node['children'] = collections.OrderedDict()
			node['children']['topics'] = collections.OrderedDict()
			node['children']['topics']['@type'] = 'attached'
			node['children']['topics']['topic']=[]
			handleOutline(children, node['children']['topics']['topic'])
		if type(src) == list:
			src.append(node)
		elif type(src) == collections.OrderedDict:
			src['topic'] = node
		else:
			raise Exception("invalid src type")
		topicInfo(node)
	elif t == list:
		for child in root:
			handleOutline(child, src)
	else:
		raise Exception("invalid outline")

def parseOPML(path, output):
	src = loadXML(path)
	root = src['opml']['body']['outline']
	handleOutline(root, output)

def createZip(name):
	zfile = zipfile.ZipFile(name+".xmind", 'w')
	tmp = os.path.join(os.getcwd(), 'template')
	files = os.listdir(tmp)
	for f in files:
		zfile.write(os.path.join(tmp, f), f)

	return zfile

def main(src):
	tar = os.path.splitext(src)[0]
	zfile = createZip(tar)
	content = os.path.join(os.getcwd(), "content.xml")

	template = loadXML(os.path.join(os.getcwd(), "template/content.xml"))
	root = template['xmap-content']['sheet']
	parseOPML(src, root)
	writeXML(template, content)

	zfile.write(content, "content.xml")
	zfile.close()

if __name__ == '__main__':
	main(sys.argv[1])
