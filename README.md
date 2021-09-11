# Oboder

A extremely small library implementing an OBO file reaDER.


## Installation

```bash
pip install -U "oboder @ git+https://github.com/aedera/oboder.git"
```

## Usage

```python
import oboder

# read a given obo file, rels=True includes other relationships in addition to 'is_a'
go = oboder.read('data/go.obo', with_rels=True)

# get a set containing ancestors of a given GO term for all relationships
anc = go.get_ancestor_set('GO:0017011')

# or ancestors for a specific relation
anc = go.get_ancestor_set('GO:0017011', rels=['part_of'])

# get a list where elements are branches of ancestors
branches = go.get_ancestors('GO:0017011')

# loop over the terms in the obo file
for t in go.ont.keys():
  print(go.ont[t])
```

In addition, oboder can be used to explore an OBO file, for example, by exploring
specific GO terms.

```python
go.ont['GO:0019538']
```
this returns a dict with the following information of the term 'GO:0019538'

```
{
'is_a': ['GO:0043170', 'GO:0044238'],
'part_of': [],
'has_part': [],
'regulates': [],
'negatively_regulates': [],
'positively_regulates': [],
'occurs_in': [],
'ends_during': [],
'happens_during': [],
'alt_ids': {'GO:0006411'},
'is_obsolete': False,
'id': 'GO:0019538',
'name': 'protein metabolic process',
'namespace': 'biological_process',
'children': {'GO:0045558', 'GO:1901142', ..., 'GO:0072376'}
}
```
