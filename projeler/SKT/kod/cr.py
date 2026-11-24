import sys,json,urllib.request,urllib.parse
for d in sys.argv[1:]:
    try:
        r=urllib.request.urlopen('https://api.crossref.org/works/'+urllib.parse.quote(d),timeout=25)
        m=json.load(r)['message']; a=', '.join(x.get('family','')+' '+x.get('given','')[:1] for x in m.get('author',[])[:8])
        print(d,'|',a,'|',m.get('issued',{}).get('date-parts'),'|',m['title'][0][:140],'|',(m.get('container-title') or [''])[0],m.get('volume'),m.get('issue'),m.get('page'))
    except Exception as e: print(d,'HATA',e)
