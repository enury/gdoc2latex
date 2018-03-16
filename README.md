# Converting a GoogleDoc to LaTeX

At the end of my PhD, I had to quickly convert a bunch of Google doc chapters into LaTeX, so I wrote this small script. It converts the HTML version of your gdoc and works best if you kept layout modifications to a minimum.

The script uses regular expressions to locate relevant `<p>` and `<span>` elements in the HTML. Here are the features of the HTML that are converted into LaTeX.

## Title and Headings
The document title becomes a chapter title `\chapter{...}`, and all headings are transformed into their LaTeX equivalent: from `<h1>` becoming a `\section{}`, all the way to `<h5>` for a `\subparagraph{}`.

## Page layout  (italics, bold, etc.)
It is best to keep those to only a few, and try not to combine them! I have limited myself to six layout features: 
1) italics: `\emph{...}`
2) bold: `\textbf{...}`
3) bold italics: `\emph{\textbf{...}}`
4) underline: `\underline{...}`
5) codetext: `\texttt{...}` (for snippets of text in sans serif)
6) quotation: within a `quotation` environment (I changed the indentation of quotation paragraphs).

These features are encoded in the HTML as class attributes to `<p>` and `<span>` elements, as the letter 'c' followed by a number. For instance `<span class="c0">` may indicate a span of text in italics. The main issue with the class numbers is that they are not consistent across documents. Even the same document may have a different class for italics, if you refresh the page and download it again! So you have to check numbers before applying the transformation. You can set the class numbers as variables at the start of the script.

## Special characters
Although the main text was in English, I had plenty of accented letters from quotations in French, Italian and German, plus a few special characters like the _e caudata_ &#281; and &amp;. This also includes all kinds of characters like quotation marks or apostrophes, which are all HTML entities that must be transformed into LaTeX. For example: the _e caudata_ `&#281;` becomes `\c{e}`, and `&amp;` becomes `\&`. I've been filling this list as I went along, so it's definitely not exhaustive! You may want to add your own.

## Images
Images in the gdoc file are also included in a separate `images` folder when you download the HTML. Images keep their original extension, but are renamed as 'image1', 'image2' etc. As I had images in each chapter, I needed to add an indication of the chapter number so that there would be no conflict. To rename an entire folder of images, I have used the following command in the terminal, here for chapter 2:

`dir | rename-item -NewName {$_.name -replace "image","image2-"}`

When replacing the HTML tags `<img src="path">`, I have used `\includegraphics{path}` in a `figure` environment. For the path to be correct, after I modified the image names, the chapter number is also needed: that's why it is a variable that must be set at the beginning of the script.

You will need to resize the images in the LaTeX, so don't waste too much time in gdoc to set images at a proper size and place.

## Footnotes
Footnotes and comments have the same structure in the HTML: in the text, there is a `<sup>` element that contains the link to the footnote/comment, for instance `<sup><a href="#ftnt1" id="ftnt_ref1">[1]</a></sup>`. At the end of the documents there will be a paragraph with the corresponding link, `<p class="..."><a href="#ftnt_ref1" id="ftnt1">[1]</a>...</p>`.

It was a bit tricky to deal with footnotes with just regular expression (here an XSLT transformation might come useful)! I managed to improvise something that worked for me. You may want to check that you have the right number of footnotes.

I didn't include comments, but in theory the code for footnotes could be adapted for comments as well.

## Lists
There are two types of lists: 
1. `<ul>` is an unordered list, therefore converted to the `itemize`environment
2. `<ol>` is an ordered list, converted to the `enumerate` environment 

In both lists, the elements `<li>...</li>` are transformed to `\item ...`.

## Tables
Tables can also be converted to LaTeX. The `<table>` elements maps to the `table`environmnent, and `<tbody>` to the `tabular` environment. A new row `<tr>`starts an new line, and the closing tag of the row plus last cell `</td></tr>` is converted to `\\`. The closing tag of the other cells `</td>` are converted to ` &`.

I add a newline before each opening paragraph `<p>`, so that the LaTeX file will keep the paragraph division from the text. However, it means that `<p>` elements inside cells also get a newline, which caused some trouble. I deleted them by hand in LaTeX, but if you have many tables, you may want to find a better solution (for instance remove `<p>` elements only inside the `<table>`).

Again, it's a very basic solution. It's better to keep your gdoc tables as simple as possible, and to improve them later in LaTeX.

## Links
Finally, any link still present is also converted. For instance `<a class="..." href="...">link</a>` is converted to `\url{link}`. I didn't use the `href` attribute, because google adds a lot of stuff around the actual link.

---

That's it! 

After you've done the transformation, there are some little things to take care of: delete the text of footnotes and comments left over at the end of the document. If you had included a table of content in the gdoc, delete also the links. Now you can spend time to arrange your tables and images. And of course, add cross-references and bibliographic citations if needed.
