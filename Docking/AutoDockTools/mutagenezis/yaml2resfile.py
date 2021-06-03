import yaml

with open('config.yaml') as c:
    config = yaml.load(c)

first_line="""
NATRO # default command that applies to everything without a non- default setting; do not repack\n
start\n\n\n\n
"""
for mutation in config['MUTAGENEZIS']:
    file_name=''
    text=""
    for m in mutation['MUTANT']:
        file_name=file_name+m['aa']+','+str(m['pos'])+','
        text=text+str(m['pos'])+" "+m['chain']+" PIKAA "+m['aa']+"\n"

    f=open('SELECTED/'+file_name+'.resfile','w')
    f.write(first_line)
    f.write(text)
    f.close()
