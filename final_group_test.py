# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 15:17:26 2020

@author: u03132tk
"""

import primer3 as p3
primers= ["CGCCGGTTCTTCTCCAGTTCCA",
"CAGATCACCCACCGCAACCTGTGT",
"CCTTCTGGGCGAACGGTTCAATCA",
"CGTCAAGTCCCAGGAGAGCTGACA",
"GCGGAAAGGAGACCAGAGCACAT",
"CGAGTTCTCGTTGTGCAGGAAGATCTC",
"TGCGTGACCTCGGCATCAACT",
"AACATCCCGATCAGCTGGTGGAA"]
homos=[]
temperatures=list(range(0,100))
heteros=[]
temperaturesBadHo=[]
temperaturesBadHet=[]
dna_conc=list(range(0,250))
for primer in primers:
    for temp in temperatures:
        for concen in dna_conc:
            homo=p3.calcHomodimer(primer, dntp_conc=0,dna_conc=concen, temp_c=temp)
            #hair=p3.calcHairpin(primer, dntp_conc=0,dna_conc=concen, temp_c=temp)
            if homo.dg<-9000:# or hair.tm>50:
                temperaturesBadHo.append(temp)
                homos.append(homo.dg)
#            print ('SEQUENCE:  ', primer)
#            print ('TEMPERATURE:  ', temp)
#            print ('OBJECT:  ',homo)
#            print ('\n\n')

for primer1 in primers:
    for primer2 in primers:
        if primer1 != primer2:
            for temp in temperatures:
                for concen in dna_conc:
                    hetero=p3.calcHeterodimer(primer1,primer2, dntp_conc=0,dna_conc=concen, temp_c=temp)
                    if hetero.dg<-9000:
                        heteros.append(hetero.dg)
                        temperaturesBadHet.append(temp)
#                    if True:
#                        print ('SEQUENCE:  ', primer1,'     ',primer2)
#                        print ('TEMPERATURE:  ', temp)
#                        print ('OBJECT:  ',hetero)
#                        print ('\n\n')
                    