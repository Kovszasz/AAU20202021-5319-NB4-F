import yaml

yaml_payload={'MUTAGENEZIS':[],'INPUT':{'PDB':'1CEX'}}
mutant=[]
mutation=1
yaml_payload['MUTAGENEZIS'].append({'MUTANT':[]})
with open('mutations.csv','r') as mutations:
    for row in mutations:
        row=list(row)
        row.pop()
        row=''.join(row)
        row=row.split(',')
        if int(row[0]) !=mutation:
            yaml_payload['MUTAGENEZIS'].append({'MUTANT':mutant})
            mutation = int(row[0])
            mutant=[]
        mutant.append({'aa':row[1],'pos':int(row[2]),'chain':row[3]})


with open('config.yaml', 'w') as file:
    documents = yaml.dump(yaml_payload, file)