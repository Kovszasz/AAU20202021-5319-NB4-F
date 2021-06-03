from matplotlib import pyplot as plt
import argparse
import numpy as np
from os import listdir
from scipy.optimize import curve_fit
from scipy.stats import norm


my_parser = argparse.ArgumentParser(description='List the content of a folder')
my_parser.add_argument('--scorefile',action='store',type=str,help='Provide the scorefile (.sc)',required=True)
my_parser.add_argument('--export_as_req_file',type=str,action='store',help='Req filter file will be exported which can be used for DesignSelect.pl script of Rosetta')#,required=True)
my_parser.add_argument('--specify_filter_params',type=str,action='store',help='Here, you can specify which parameters should be investigated which can be used for further filtering')#,required=isinstance(my_parser.export_as_req_file,str))
my_parser.add_argument('--score_file_sorting',type=str,action='store',help='Sortmin argument in the req file for DesignSelect.pl',default='total_score')
my_parser.add_argument('--filter_rate',type=int,action='store',default=1,help='Here can be set wether 1mu, 2mu or 3mu *mean of the distribution should be selected')
args = my_parser.parse_args()
scorefile = args.scorefile
export_as_req_file=args.export_as_req_file
specify_filter_params=args.specify_filter_params
score_file_sorting=args.score_file_sorting
filter_rate=args.filter_rate

def extract_keys(line):
    return_dict={}
    for l in line:
        if isinstance(l,str) and len(l)>0:
            return_dict[l]=[]
    return return_dict

def add_values(line):
    clean_line=[]
    for l in line:
        if isinstance(l,str) and len(l)>0:
            try:
                clean_line.append(float(l))
            except:
                pass
#                clean_line.append(l)
    for k in range(len(keys)):
        scores[keys[k]].append(clean_line[k])
    

# Define model function to be used to fit to the data above:
def gauss(x, *p):
    A, mu, sigma = p
    return A*numpy.exp(-(x-mu)**2/(2.*sigma**2))


def determine_treshold(value):
    #return np.mean(value)
    print(min(value),'\t',max(value),'\t',np.mean(value))
    mu, std = norm.fit(value)
    #mean=np.mean(value)
    #min_=min(value)
    #max_=max(value)
    r=mu-filter_rate*std
    nb=[i for i in value if i<r]
    print(len(nb))
    return r


scores={}
keys=[]
with open(scorefile,'r') as sc:
    for line in sc:
        line=line.replace('SCORE:','')
        line=line.replace('\n','')
        line=line.replace('description','')
        line=line.split(' ')
        if len(scores.keys())==0:
            scores=extract_keys(line)
            keys=list(scores.keys())
        else:
            add_values(line)
if specify_filter_params is None:
    specify_filter_params=list(scores.keys())
else:
    specify_filter_params=specify_filter_params.split(',')

result={}
for k in scores.keys():
    if k in specify_filter_params:
        print(k)
        result[k]=determine_treshold(scores[k])

if export_as_req_file:
    f=open(export_as_req_file,'w')
    for r in result.keys():
        f.write('req '+r+' value < '+str(result[r])+'\n')
    f.write('output sortmin '+score_file_sorting)
    f.close()





