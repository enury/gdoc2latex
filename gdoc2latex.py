#!/usr/bin/env python3

import re
import sys

#path to google doc file
filename = '2-1-Collation'
gdoc_path = filename+'.html'
    
#load the text of the file into a variable html
with open(gdoc_path, 'r', encoding='utf-8') as infile:
    html = infile.read()

#delete <head> content
head = re.compile(r'<head.+?</head>')
html = head.sub(r'', html)
    
#------------------------------------
#-------- titles & headings ---------

h1 = re.compile(r'<h1.*?>(.*?)</h1>')
html = h1.sub(r'\n\\section{\1}', html)

h2 = re.compile(r'<h2.*?>(.*?)</h2>')
html = h2.sub(r'\n\\subsection{\1}', html)

h3 = re.compile(r'<h3.*?>(.*?)</h3>')
html = h3.sub(r'\n\\subsubsection{\1}', html)

h4 = re.compile(r'<h4.*?>(.*?)</h4>')
html = h4.sub(r'\n\\paragraph{\1}', html)

h5 = re.compile(r'<h5.*?>(.*?)</h5>')
html = h5.sub(r'\n\\subparagraph{\1}', html)

    
#------------------------------------
#----- italics/bold/underlined ------

#ATTENTION: check span class number for each document.

#Italics
i = re.compile(r'<span class="c11">(.*?)</span>')
html = i.sub(r'\\emph{\1}', html)

#bold
b = re.compile(r'<span class="c7">(.*?)</span>')
html = b.sub(r'\\textbf{\1}', html)

#underline
#u = re.compile(r'<span class="c0">(.*?)</span>')
#html = u.sub(r'\\underline{\1}', html)

#quotations
q = re.compile(r'<p class="c15 c26">(.*?)</p>')
html = q.sub(r'\n\\begin{quotation}\n\1\n\\end{quotation}\n', html)

#------------------------------------
#-----replace special characters-----

#whitespace
html = re.sub(r'&nbsp;',r' ',html)

#quotation marks
html = re.sub(r'&quot;',r"'",html)
html = re.sub(r'&ldquo;',r"'",html)
html = re.sub(r'&rdquo;',r"'",html)
html = re.sub(r'&rsquo;',r"'",html)
html = re.sub(r'&#39;',r"'",html)

html = re.sub(r'&rlquo;',r"`",html)
html = re.sub(r'&lsquo;',r"`",html)

#dashes
html = re.sub(r'&mdash;',r'---',html)
html = re.sub(r'&ndash;',r'---',html)#check if there are real n-dashes

#accents
html = re.sub(r'&aring;',r'{\aa}',html)#a hakanson
html = re.sub(r'&ccedil;',r'\c{c}',html)
html = re.sub(r'&eacute;',r'é',html)
html = re.sub(r'&ecirc;',r'ê',html)
html = re.sub(r'&egrave;',r'è',html)
html = re.sub(r'&auml;',r'ä',html)
html = re.sub(r'&Auml;',r'Ä',html)
html = re.sub(r'&ouml;',r'ö',html)
html = re.sub(r'&uuml;',r'ü',html)
html = re.sub(r'&szlig;',r'ss',html)
html = re.sub(r'&agrave;',r'à',html)
html = re.sub(r'&igrave;',r'ì',html)
html = re.sub(r'&ograve;',r'ò',html)
html = re.sub(r'&ugrave;',r'ù',html)

html = re.sub(r'&esect;',r'§',html)

#html = re.sub(r'&ecirc;',r'ê',html)
#html = re.sub(r'&ecirc;',r'ê',html)


#------------------------------------
#-------------- IMAGES --------------
img = re.compile(r'<img.+?src="(.+?)".+?>')
html = img.sub(r'\n\\begin{figure}\n\\includegraphics{\1}\n\\caption{}\n\\label{}\n\\end{figure}\n', html)

#------------------------------------
#------------ FOOTNOTES -------------

#two types of <sup> for footnote, with or without a class attribute
ftnt = re.compile(r'<sup><a href="#ftnt(\d+?)".*?</sup>')
ftnt2 = re.compile(r'<sup class="c\d+"><a href="#ftnt(\d+?)".*?</sup>')

nb = ftnt.subn(r'\\footnote{ftnt_ref\1i}', html)
html = nb[0]

nb2 = ftnt2.subn(r'\\footnote{ftnt_ref\1i}', html)
html = nb2[0]

j = nb[1]+nb2[1]
print(j)

for i in range(1, j+1):
    string = '<p class="c\d+"><a href="#ftnt_ref{0}" id.*?</p>'.format(str(i))
    match = re.search(string, html, re.MULTILINE)
    if match:
        html = re.sub('ftnt_ref'+str(i)+'i', match.group(), html)
    else:
        pass
        print(i)

#delete [] in footnotes and comments references
html = re.sub(r'<a href="#ftnt_ref.*?</a>', r'', html)
html = re.sub(r'<a href="#cmnt\d.*?</a>', r'', html)

#------------------------------------
#-------------- LISTS ---------------
html = re.sub(r'<ul.*?>', r'\n\\begin{itemize}', html)
html = re.sub(r'</ul>', r'\n\\end{itemize}', html)
html = re.sub(r'<ol.*?>', r'\n\\begin{enumerate}', html)
html = re.sub(r'</ol>', r'\n\\end{enumerate}', html)

html = re.sub(r'<li.*?>(.+?)</li>', r'\n\\item \1', html)

#------------------------------------
#-------------- TABLES ---------------

#<table>...</table>


#------------------------------------
#-------------- SAVE ----------------

#keep paragraph separations
html = re.sub(r'<p', r'\n<p', html)

#delete rest of html tags
html = re.sub(r'<.+?>',r'',html)

new_gdoc_path = 'LATEX-'+filename+'.html'

#save
with open(new_gdoc_path, 'w', encoding='utf-8') as outfile:
    outfile.write(html)
