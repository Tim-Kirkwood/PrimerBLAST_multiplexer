# PrimerBLAST_multiplexer

newprimer_sheet.py - script to collate primerBLAST outputs into single excel table.

Grouper.py - Script to identify groups of primers that are not predicted to heterodimerise (dG >-7000cal, at 37 degrees, as calculated by primer3) using the collated primer outputs of primerBLAST (reads in excel sheet of newprimer_sheet.py as a pandas dataframe).  Primers in a group are compared to all other members of a group.  Groups are only included if they are <90% similar to those included in groups list already.

final_group_test.py - script to take final group and predict the maximum temperature that heterodimerisation is predicted to occur at.
