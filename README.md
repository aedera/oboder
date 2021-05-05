# Oboder

Oboder is a very small python library containing an OBO file reaDER.


# Installation

```bash
pip install -U oboder @ git+https://github.com/aedera/oboder.git"
```

# Usage

```python
import oboder
go = oboder.read('data/go.obo')

# get ancestors of a given GO term
go.get_ancestor_set('GO:0017011')
```
