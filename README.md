# Oboder

Oboder is a very small python library implementing an OBO file reaDER.


## Installation

```bash
pip install -U "oboder @ git+https://github.com/aedera/oboder.git"
```

## Usage

```python
import oboder

# read a given obo file
go = oboder.read('data/go.obo')

# get a set containing ancestors of a given GO term
anc = go.get_ancestor_set('GO:0017011')

# get a list where each element is a branch of ancestors
branches = go.get_ancestors('GO:0017011')

# loop over the terms in the obo file
for t in go.ont.keys():
  print(go.ont[t])
```
