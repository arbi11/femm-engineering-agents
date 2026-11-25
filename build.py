"""Build the article pages with Python's standard library; no external services."""
from pathlib import Path
from html import escape
import json
import re

ROOT=Path(__file__).resolve().parent

def inline(text):
    text=escape(text,quote=False)
    text=re.sub(r'`([^`]+)`',r'<code>\1</code>',text)
    text=re.sub(r'\[([^]]+)\]\(([^\s)]+)\)',r'<a href="\2">\1</a>',text)
    text=re.sub(r'\*\*(.+?)\*\*',r'<strong>\1</strong>',text)
    return re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<em>\1</em>',text)

def page(title,body,css,description=''):
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>'+escape(title)+'</title><meta name="description" content="'+escape(description,quote=True)+'">'
            '<link rel="stylesheet" href="'+css+'"></head><body>'+body+'</body></html>\n')

def article_body(source):
    out=[]
    for chunk in re.split(r'(```[^\n]*\n.*?\n```)',source,flags=re.S):
        if chunk.startswith('```'):
            language,code=chunk[3:].split('\n',1);code=code[:-4]
            out.append('<pre data-code-block-mode="1" data-code-block-lang="'+escape(language,quote=True)+
                       '"><code class="language-'+escape(language,quote=True)+'">'+escape(code)+'</code></pre>')
            continue
        paragraphs=chunk.strip().split('\n\n');i=0
        while i<len(paragraphs):
            p=paragraphs[i].strip();i+=1
            if not p:continue
            m=re.fullmatch(r'!\[([^]]+)\]\(([^)]+)\)',p)
            if m:
                figure='<figure><img src="'+escape(m[2],quote=True)+'" alt="'+escape(m[1],quote=True)+'">'
                if i<len(paragraphs) and re.match(r'^\*(Figure|Equation)\b',paragraphs[i]):
                    figure+='<figcaption>'+inline(paragraphs[i].strip('*'))+'</figcaption>';i+=1
                out.append(figure+'</figure>')
            elif p.startswith('## '):out.append('<h2>'+inline(p[3:])+'</h2>')
            elif p.startswith('> '):out.append('<blockquote><p>'+inline(' '.join(line.lstrip('> ') for line in p.splitlines()))+'</p></blockquote>')
            else:out.append('<p>'+inline(p.replace('\n',' '))+'</p>')
    return '\n'.join(out)

articles=[]
for number in range(1,6):
    source=ROOT/f'part-{number}/index.md'
    title,body=source.read_text().split('\n\n',1);title=title.lstrip('# ')
    subtitle=body.split('\n\n',1)[0].strip('*')
    nav=[]
    if number>1:nav.append(f'<a href="../part-{number-1}/index.html">Previous: Part {number-1}</a>')
    if number<5:nav.append(f'<a href="../part-{number+1}/index.html">Next: Part {number+1}</a>')
    content=('<header class="site-bar"><a href="../index.html">FEMM and Engineering Agents</a></header>'
             '<main><article><h1>'+escape(title)+'</h1><p class="byline">By Arbaaz Khan</p>'+
             article_body(body)+'</article><nav class="series-nav" aria-label="Series">'+
             ' · '.join(nav)+'</nav><footer><a href="index.md">Markdown source</a></footer></main>')
    (source.parent/'index.html').write_text(page(title,content,'../assets/site.css',subtitle))
    articles.append({'part':number,'title':title,'subtitle':subtitle})

items=''.join('<li><a href="part-'+str(a['part'])+'/index.html"><h2>'+escape(a['title'])+
              '</h2></a><p>'+escape(a['subtitle'])+'</p></li>' for a in articles)
index=('<main class="series-index"><p class="eyebrow">A worked series by Arbaaz Khan</p>'
       '<h1>FEMM and Engineering Agents</h1><p class="lede">From a first magnetic-field model '
       'to checking an AI agent’s experiment and reconstructing a published motor.</p>'
       '<ol class="contents">'+items+'</ol><footer><a href="README.md">Repository and import instructions</a>'
       ' · <a href="examples/index.html">Companion files</a></footer></main>')
(ROOT/'index.html').write_text(page('FEMM and Engineering Agents',index,'assets/site.css'))

example_links=[]
for number in range(1,6):
    folder=ROOT/f'examples/part-{number}'
    files=sorted(p for p in folder.rglob('*') if p.is_file() and p.name!='index.html')
    links=''.join('<li><a href="'+escape(str(p.relative_to(folder)),quote=True)+'">'+
                  escape(str(p.relative_to(folder)))+'</a></li>' for p in files)
    setup=('<p><a href="../SETUP_Articles_2-4.txt">Setup for Articles 2–4</a></p>' if number in [2,3,4]
           else '<p>Use the setup in Article 1 and the pinned native FEMM environment.</p>')
    body=('<main><p><a href="../../part-'+str(number)+'/index.html">Back to the article</a></p>'
          '<h1>Part '+str(number)+': companion files</h1>'+setup+'<ul>'+links+'</ul></main>')
    (folder/'index.html').write_text(page(f'Part {number} companion files',body,'../../assets/site.css'))
    example_links.append(f'<li><a href="part-{number}/index.html">Part {number}</a></li>')
(ROOT/'examples/index.html').write_text(page('Companion files','<main><h1>Companion files</h1><ul>'+
     ''.join(example_links)+'</ul><p><a href="../index.html">Series</a></p></main>','../assets/site.css'))
print(json.dumps({'article_pages':len(articles),'root':str(ROOT)}))
