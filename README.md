# qiime_scripts
A few scripts that Rob has written to handle qiime files. This is not something we do all the time, but occassionally someone asks us to munge the data into a particular format.

You are welcome to use the scripts and/or use them as inspiration. You're on your own if you do.

# number_taxonomy.py

Here is the question:

I need the attached otu_tablex.biom to look like the otu_tableQIME.biom, so the numbers in brackets after each classification need to be removed and the k_ / p_/ etc. needs to be added to the front of each classification. 

i.e. from this:

```
"rows": [{"id": "OTUId", "metadata": {"taxonomy": ["None"]}},{"id": "OTU_1;size=18783;", "metadata": {"taxonomy": ["Bacteria(100.0),\"Proteobacteria\"(45.0),Alphaproteobacteria(33.1),Rhizobiales(33.1),Rhizobiaceae(33.1),Kaistia(33.1)"]}},{"id": "OTU_2;size=7463;", "metadata": {"taxonomy": ["Bacteria(100.0),\"Actinobacteria\"(66.7),Actinobacteria(52.0),Actinomycetales(48.6),Nocardioidaceae(41.2),Nocardioides(39.7)"]}}
```

to this:

```
"rows": [{"id": "denovo0", "metadata": {"taxonomy": ["k__Bacteria", "p__Bacteroidetes", "c__[Saprospirae]", "o__[Saprospirales]", "f__Chitinophagaceae", "g__Sediminibacterium", "s__"]}},{"id": "denovo1", "metadata": {"taxonomy": ["Unassigned"]}},{"id": "denovo2", "metadata": {"taxonomy": ["k__Bacteria", "p__Proteobacteria", "c__Betaproteobacteria", "o__Burkholderiales", "f__Comamonadaceae", "g__", "s__"]}}
```

This script uses our ncbi taxonomy module to create the list.


