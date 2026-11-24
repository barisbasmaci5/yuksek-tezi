"""pandoc çıktısındaki çizelgeleri kenarlıklı, tam genişlik ve okunur hâle getirir."""
import sys, re, zipfile
src, out = sys.argv[1], sys.argv[2]
z = zipfile.ZipFile(src); files = {n: z.read(n) for n in z.namelist()}
d = files['word/document.xml'].decode('utf8')
brd = ('<w:tblBorders><w:top w:val="single" w:sz="6" w:color="808080"/><w:left w:val="nil"/><w:bottom w:val="single" w:sz="6" w:color="808080"/>'
       '<w:right w:val="nil"/><w:insideH w:val="single" w:sz="2" w:color="BFBFBF"/><w:insideV w:val="nil"/></w:tblBorders>')
d = d.replace('<w:tblStyle w:val="Table" />', '')
d = d.replace('<w:jc w:val="start" /><w:tblCaption', '<w:jc w:val="center" />' + brd + '<w:tblLayout w:type="autofit"/><w:tblCaption')
d = re.sub(r'(<w:tblPr>)(?![^<]*<w:tblBorders)', r'\1', d)
# hücre paragraflarında 9 pt
d = d.replace('<w:pStyle w:val="Compact" />', '<w:pStyle w:val="Compact" /><w:spacing w:before="20" w:after="20"/><w:rPr><w:sz w:val="18"/></w:rPr>')
files['word/document.xml'] = d.encode('utf8')
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zo:
    for n in z.namelist(): zo.writestr(n, files[n])
