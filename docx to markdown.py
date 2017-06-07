import mammoth
import os
path=r'C:\temp\психология'
save_path=r'C:\temp\психология\save'
#adding navigation links and header
beg='<a href=README.md><img src="../img/back.jpg" width="50" height="50" /></a><p><h1>%s</h1></p><p>'
end='<a href=README.md><img src="../img/back.jpg" width="50" height="50" /></a>'

def process_docx(filename):
    with open(os.path.join(path,filename), "rb") as docx_file:
        result=mammoth.convert_to_html(docx_file)
        print(filename,result.messages)
        f_name=filename[:-5]
        with open(os.path.join(save_path,f_name+'.md'), "w", encoding='utf-8') as text_file:
            text_file.write(beg % f_name+result.value+end)
for file in os.listdir(path):
    if file.endswith(".docx"):
        process_docx(file)
