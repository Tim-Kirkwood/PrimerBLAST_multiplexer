# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 19:01:32 2020

@author: u03132tk
"""
import pandas as pd



#test_url='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?ctg_time=1587734808&job_key=cXuueqqNpyWAHzcaOnoTKEBhAhptchkHbA'
url_cluster5_20bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?ctg_time=1597687186&job_key=PzXgWgT8CVQuagxvAQ8oXXsUOW9WByJyVw'
url_cluster5_25bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?ctg_time=1597687482&job_key=Jy34Qf-O8ibVHGIZb3lGKxViVxk4cUwEOQ'
url_cluster5_30bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?job_key=GxHEfiD8LVQKaihvJQ8MXV8UHW9yBwZycw'
url_cluster8_20bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?job_key=CwHUbjD8PVQaajhvNQ8cXU8UDW9iBxZyYw'
url_cluster8_25bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?job_key=ODLnXuCO7SbKHH0ZcHlZKwpiSBkncVMEJg'
url_cluster8_30bp=None
url_cluster17_20bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?ctg_time=1597687832&job_key=xM4boh2PECc3HYAYjXikKvdjtRjacK4F2w'
url_cluster17_25bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?ctg_time=1597687855&job_key=k5lMRzx3Md8W4SvkJoQP1lyfHuRxjAX5cA'
url_cluster17_30bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?job_key=zccSqxSPGSc-HYkYhHitKv5jvBjTcKcF0g'
url_cluster22_20bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?ctg_time=1597687928&job_key=q6F0fwR3Cd8u4RPkHoQ31mSfJuRJjD35SA'
url_cluster22_25bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?ctg_time=1597687970&job_key=pqx5cgl3BN8j4R7kE4Q61mmfK-REjDD5RQ'
url_cluster22_30bp='https://www.ncbi.nlm.nih.gov/tools/primer-blast/primertool.cgi?ctg_time=1twJsA-PAiclHZIYn3i2KuVjpxjIcLwFyQ'


cluster_urls=[(5,url_cluster5_20bp),
              (8,url_cluster8_20bp),
              (17,url_cluster17_20bp),
              (22,url_cluster22_20bp),
              (5,url_cluster5_25bp),
              (8,url_cluster8_25bp),
              (17,url_cluster17_25bp),
              (22,url_cluster22_25bp),
              (5,url_cluster5_30bp),
              (8,url_cluster8_30bp),
              (17,url_cluster17_30bp),
              (22,url_cluster22_30bp)]

primer_blast_params_list=[]
dataframe_out= pd.DataFrame()
primer_pair=0
print ('Empty dataframe built')

for cluster in cluster_urls:
    cluster_number=cluster[0]
    url=cluster[1]#output of primer blast
    if url != None:
        tables = pd.read_html(url)
        #get running params
        primer_blast_params_list.append(('cluster number:  '+str(cluster_number), tables[0])) 
        for dataframe in tables[1::]:
            productlength=dataframe['Length'][3]
            newdata=dataframe.drop([2,3,4,5,6,7])
            newdata['primer_pair']=primer_pair#group forward and reverse primer pairs
            newdata['product length']=productlength#allow sorting by product length
            newdata['cluster']=cluster_number
            dataframe_out=dataframe_out.append(newdata, ignore_index=True)
            primer_pair+=1
dataframe_out.to_excel("rawdataframe_out.xlsx", sheet_name='Sheet_name_1')
print ('Full dataframe made')