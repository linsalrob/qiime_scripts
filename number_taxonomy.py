#!/usr/bin/env python

import json
import sys
import os
from pprint import pprint
import re
import taxon


taxa = None
names = None

def climb_taxonomy(tid):
    global taxa
    global names
    rtax = {'superkingdom':'__', 'phylum':'__', 'class':'__', 'order':'__', 'family':'__', 'genus':'__', 'species':"__"}
    rtax[taxa[tid].rank] = names[tid].name
    while taxa[tid].parent != '1' and i != '1':
        if (taxa[tid].rank in rtax):
            rtax[taxa[tid].rank] = names[tid].name
        tid = taxa[tid].parent


try:
    f = sys.argv[1]
except:
    sys.exit(sys.argv[0] + " json format file")

with open(f, 'r') as json_file:
    data = json.load(json_file)

sys.stderr.write("Reading the taxonomy:\n")
taxa = taxon.readNodes()
names,blastname = taxon.readNames()
sys.stderr.write("Done reading taxonomy\n")


# figureing out species, genus, ranks, etc

# need to have:
    # kingdom phylum class order family genus species
kingdom={}
phylum={}
t_class={}
order={}
family={}
genus={}
species={}

want = {'superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species'}

for t in taxa:
    if taxa[t].rank in want:
        if (taxa[t].rank == 'superkingdom'):
            kingdom[names[t].name]="k_" + t
        elif (taxa[t].rank == 'phylum'):
            phylum[names[t].name]="p_" + t
        elif (taxa[t].rank == 't_class'):
            t_class[names[t].name]="c_" + t
        elif (taxa[t].rank == 'order'):
            order[names[t].name]="o_" + t
        elif (taxa[t].rank == 'family'):
            family[names[t].name]="f_" + t
        elif (taxa[t].rank == 'genus'):
            genus[names[t].name]="g_" + t
        elif (taxa[t].rank == 'species'):
            species[names[t].name]="s_" + t


for r in data['rows']:
    #pprint(r['metadata']['taxonomy'])
    newtax = []
    for t in r['metadata']['taxonomy']:
        temptax = []
        for p in t.split(','):
            q = re.sub('\([\d\.]+\)', '', p)
            q = q.replace('"', '')
            #print(p + "\n" + q + "\n")
            temptax.append(q)
        # now work from the back and see if we have an element
        rtax = None
        while (temptax):
            test = temptax.pop()
            if (test in species):
                rtax = climb_tax(species[test])
                temptax = None
            elif (test in genus):
                rtax = climb_tax(genus[test])
                temptax = None
            elif (test in family):
                rtax = climb_tax(family[test])
                temptax = None
            elif (test in order):
                rtax = climb_tax(order[test])
                temptax = None
            elif (test in t_class):
                rtax = climb_tax(t_class[test])
                temptax = None
            elif (test in phylum):
                rtax = climb_tax(phylum[test])
                temptax = None
            elif (test in kingdom):
                rtax = climb_tax(kingdom[test])
                temptax = None

        newtax.append(",".join(rtax))
    pprint(r['metadata']['taxonomy'])
    pprint(newtax)
    r['metadata']['taxonomy']=newtax

with open('repout.biom', 'w') as json_out:
    json.dump(data, json_out)
        

