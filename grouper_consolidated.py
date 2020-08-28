# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 20:19:14 2020

@author: u03132tk
"""

import pandas as pd
import primer3 as p3
def in_group(group_list, group_current, similarity_threshold):
    len_group_current=len(set(group_current))
    for group in group_list:
        len_group=len(set(group))
        duplicates=len(set(group) & set(group_current))
        if 100*(duplicates/max(len_group, len_group_current))>similarity_threshold:
            return True
        
        
        
        


dataframe_of_primers=pd.read_excel('rawdataframe_out_delcolA.xlsx')

seq_list=list(dataframe_of_primers["Sequence (5'->3')"])
primer_list=list(dataframe_of_primers["primer_pair"])
cluster_list=list(dataframe_of_primers["cluster"])
seq_primer_tuple_list=list(zip(seq_list, primer_list, cluster_list))#[(seq,primer pair),(seq, primer pair)]
groups=[]
groups_tested_incomplete_pairs=[]
groups_tested_incompleteclusters=[]
highDg=[]
dataframe_groups=[]
help_list=[]
#group_out_list=[]
#oligo 250,  
too_similar=[]
for primerituple in seq_primer_tuple_list:#make group from perspective of each primer
    #in_group=[]
    if len(groups)<3:
        primeri=primerituple[0]
        primeri_label=primerituple[1]
        primeri_cluster=primerituple[2]
        group=[[primeri, primeri_label, primeri_cluster]]
        firstgroup=group.copy()
        #primer_pairs=[]
        for primeriituple in seq_primer_tuple_list:
            primerii=primeriituple[0]
            primerii_label=primeriituple[1]
            primerii_cluster=primeriituple[2]
            if primeri==primerii:#when dont you care?
                continue
            if [primerii,primerii_label, primerii_cluster] in group:
                continue
            thermo_object_homo=p3.calcHomodimer(primerii,dntp_conc=0,dna_conc=250.0)
            if thermo_object_homo.dg>-8000:
                inGroup=True
                for primeriii_nest_list in group: #--> check them all against group primers - at the moment you only check against #1
                    primeriii=primeriii_nest_list[0]
                    thermo_object_hetero=p3.calcHeterodimer(primerii,primeriii,dntp_conc=0,dna_conc=250.0)
                    if thermo_object_hetero.dg<-7000:
                        highDg.append(thermo_object_hetero.dg)
                        inGroup=False
                        break
                if inGroup==True:
                    group.append([primerii, primerii_label, primerii_cluster])
                #primer_pairs.append(primerii_label)
        final_pairs=[]
        whole_sequences=[]
        group_out=[]
        group_out_details=[]
        allClusters=[]
        clusterType_out=[]
        group_primer_tuple_list=list(zip(*group))
        final_pairs=group_primer_tuple_list[1]
        allClusters=group_primer_tuple_list[2]
    #        for primer in group:
    #            final_pairs.append(primer[1])
    #            allClusters.append(primer[2])
        for pairID in final_pairs:
            if final_pairs.count(pairID)>2:
                print ('ERROR')
            if final_pairs.count(pairID)==2:
                whole_sequences.append(pairID)
        group_out_incomplete_pairs=[]
        for primer in group:#dont just say 'in all clusters' as they will all be present, you need to make sure the one getting picked which has a whole pair has a correct cluster assignment
            if primer[1] in whole_sequences:
                listIndex=group.index(primer)
                clusterType_out.append(allClusters[listIndex])
                group_out.append(primer[1])
                group_out_details.append(primer)
                #group_out_list.append(group_out)
            else:
                group_out_incomplete_pairs.append(primer)
        groups_tested_incomplete_pairs.append(group_out_incomplete_pairs)
        if len (group_out)<1:
            continue
        test5=5 in clusterType_out
        test8=8 in clusterType_out
        test17=17 in clusterType_out
        test22=22 in clusterType_out
        if test5 and test8 and test17 and test22:
            similar=in_group(groups, group_out, 90)
            if not similar:
                count5=clusterType_out.count(5)>4
                count8=clusterType_out.count(8)>4
                count17=clusterType_out.count(17)>4
                count22=clusterType_out.count(22)>4
                if count5 and count8 and count17 and count22: 
                    groups.append(group_out)
                    print ('Group added')
    #                    if len(groups)==1:
    #                        break
            else:
                too_similar.append(group_out)
        else:#maybe getting duplicate data here
            groups_tested_incompleteclusters.append(group_out_details)
    else:
        break
    
#stackoverflowpre=groups.copy()
#'''copied from https://stackoverflow.com/questions/7961363/removing-duplicates-in-lists'''
#tuple_line = [tuple(pt[4]) for pt in groups] # convert list of list into list of tuple
#tuple_new_line = set(tuple_line) # remove duplicated element
#groups_no_dup = [list(t) for t in tuple_new_line] # convert list of tuple into list of list
#''''''
#stackoverflowpost=groups_no_dup.copy()

'''turns out primerBLAST made some duplicate primers (e.g. a forward primer with two different 
reverse primers), so there are some extra primers in final datframees below.  the unwhole pairs 
get cleaned etc properly so the groups used to make the dataframes are correct, but if there is 
two sequences in the first dataframe it gets assigned to the initial group all instances get assigned 
in the final group, even if the reverse primer is not present.  not worth fixing here, just pay attention 
to primer pairs in excel - if there is only one for a sequence it should not be there''' 
for final_group in groups:#groups_no_dup:
    dataframe_cut=dataframe_of_primers.copy()
    for primer_pair in final_group:
        dataframe_cut.loc[dataframe_cut["primer_pair"] == primer_pair, 'group_test'] = 'group'
    dataframe_cut=dataframe_cut.dropna(subset=['group_test'])
    dataframe_groups.append(dataframe_cut)

        