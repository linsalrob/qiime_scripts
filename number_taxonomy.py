#!/usr/bin/env python

import json
import sys
import os
from pprint import pprint
import re
import taxon


taxa = None
names = None

def climb_tax(tid):
    global taxa
    global names
    # sys.stderr.write("Checking ID for " + tid + "\n")
    rtax = {'superkingdom':'', 'phylum':'', 'class':'', 'order':'', 'family':'', 'genus':'', 'species':""}
    # sys.stderr.write("Rank: " + taxa[tid].rank + "\n")
    # sys.stderr.write("Name: " + names[tid].name + "\n")

    rtax[taxa[tid].rank] = names[tid].name
    while taxa[tid].parent != '1' and tid != '1':
        if (taxa[tid].rank in rtax):
            rtax[taxa[tid].rank] = names[tid].name
        tid = taxa[tid].parent
    return rtax


try:
    f = sys.argv[1]
    outfile = sys.argv[2]
except:
    sys.exit(sys.argv[0] + " <json format file> <output file>")

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

want = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']

for t in taxa:
    if taxa[t].rank in want:
        if (taxa[t].rank == 'superkingdom'):
            kingdom[names[t].name]=t
        elif (taxa[t].rank == 'phylum'):
            phylum[names[t].name]=t
        elif (taxa[t].rank == 't_class'):
            t_class[names[t].name]=t
        elif (taxa[t].rank == 'order'):
            order[names[t].name]=t
        elif (taxa[t].rank == 'family'):
            family[names[t].name]=t
        elif (taxa[t].rank == 'genus'):
            genus[names[t].name]=t
        elif (taxa[t].rank == 'species'):
            species[names[t].name]=t


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
        rtax = {'superkingdom':'', 'phylum':'', 'class':'', 'order':'', 'family':'', 'genus':'', 'species':""}
        #pprint(temptax)
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
            # else:
                # sys.stderr.write(test + " not found\n")

        

        rrtax=""
        for w in want:
            if w == 'superkingdom':
                rrtax = 'k__' + rtax[w]
            else:
                rrtax += "," + w[0] + "__" + rtax[w]
        #rrtax = rrtax.replace(',', '', 1)
        newtax.append(rrtax)

    #pprint(r['metadata']['taxonomy'])
    #pprint(newtax)
    r['metadata']['taxonomy']=newtax

with open(outfile, 'w') as json_out:
    json.dump(data, json_out)
        

