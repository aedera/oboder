#!/usr/bin/env python3

# root terms
BIOLOGICAL_PROCESS = 'GO:0008150'
MOLECULAR_FUNCTION = 'GO:0003674'
CELLULAR_COMPONENT = 'GO:0005575'
FUNC_DICT = {
    'cc': CELLULAR_COMPONENT,
    'mf': MOLECULAR_FUNCTION,
    'bp': BIOLOGICAL_PROCESS,
    'cellular_component': CELLULAR_COMPONENT,
    'molecular_function': MOLECULAR_FUNCTION,
    'biological_process': BIOLOGICAL_PROCESS
}
NAMESPACES = {
    'cc': 'cellular_component',
    'mf': 'molecular_function',
    'bp': 'biological_process'
}
namespace2go = {
    'cellular_component': CELLULAR_COMPONENT,
    'molecular_function': MOLECULAR_FUNCTION,
    'biological_process': BIOLOGICAL_PROCESS
}

_allrels=[
    'is_a',
    'part_of',
    'regulates',
    'negatively_regulates',
    'positively_regulates',
    'occurs_in',
    'ends_during',
    'happens_during'
]

class Ontology(object):
    def __init__(self, filename='data/go.obo', with_rels=False, remove_obs=True, include_alt_ids=True):
        """
        if with_rels=False only consider is_a as relationship
        """
        self.fname = filename
        self.remove_obs = remove_obs
        self.include_alt_ids = include_alt_ids
        self.leaves = []
        self.ont = self.load_data(filename, with_rels)

    def load_data(self, filename, with_rels):
        ont = dict()
        obj = None
        with open(filename, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if line == '[Term]':
                    if obj is not None:
                        ont[obj['id']] = obj
                    obj = dict()
                    obj['is_a'] = list()
                    obj['part_of'] = list()
                    obj['has_part'] = list()
                    obj['regulates'] = list()
                    obj['negatively_regulates'] = list()
                    obj['positively_regulates'] = list()
                    obj['occurs_in'] = list()
                    obj['ends_during'] = list()
                    obj['happens_during'] = list()
                    obj['alt_ids'] = set([])
                    obj['is_obsolete'] = False
                    continue
                elif line == '[Typedef]':
                    if obj is not None:
                        ont[obj['id']] = obj
                    obj = None
                else:
                    if obj is None:
                        continue
                    l = line.split(": ")
                    if l[0] == 'id':
                        obj['id'] = l[1]
                    elif l[0] == 'alt_id':
                        obj['alt_ids'].add(l[1])
                        #breakpoint()
                       # avoid storing the main id as alternative id
                        # obj['alt_ids'] -= set([obj['id']])
                    elif l[0] == 'namespace':
                        obj['namespace'] = l[1]
                    elif l[0] == 'is_a':
                        obj['is_a'].append(l[1].split(' ! ')[0])
                    elif with_rels and l[0] == 'relationship':
                        it = l[1].split()
                        rel_type = it[0]
                        term_in_rel = it[1]
                        obj[rel_type].append(term_in_rel)
                        #breakpoint()
                        # add all types of relationships
                        #obj['is_a'].append(it[1])
                    elif l[0] == 'name':
                        obj['name'] = l[1]
                    elif l[0] == 'is_obsolete' and l[1] == 'true':
                        obj['is_obsolete'] = True
            if obj is not None:
                ont[obj['id']] = obj
        #
        for term_id in list(ont.keys()):
            if self.include_alt_ids:
                for t_id in ont[term_id]['alt_ids']: # add alt_ids as ontology terms
                    ont[t_id] = ont[term_id]
            if self.remove_obs and ont[term_id]['is_obsolete']:
                del ont[term_id]
        #
        # REMOVE PART OF ONTOLOGY
        # for term_id in list(ont.keys()):
        #     if ont[term_id]['namespace'] != 'cellular_component':
        #         del ont[term_id]
        #
        for term_id, val in ont.items():
            if 'children' not in val:
                val['children'] = set()
            for p_id in val['is_a']:
                if p_id in ont:
                    if 'children' not in ont[p_id]:
                        ont[p_id]['children'] = set()
                    ont[p_id]['children'].add(term_id)
        # generate leaves
        for term_id, val in ont.items():
            if len(val['children']) == 0: # no children
                root_id = FUNC_DICT[val['namespace']]
                #self.leaves[root_id].add(term_id)
                self.leaves.append(term_id)
        return ont

    def get_ancestors(self, term_id, rels=_allrels):
        if term_id not in self.ont:
            return set()

        # get parents for each specified relation
        parents = set({})
        for r in rels:
            parents |= set(self.ont[term_id][r])

        # return input term if no parents found
        if len(parents) < 1:
            return [[term_id]]

        # recursive call for each parent found
        branches = []
        for parent_id in parents:
            branches += [ b + [term_id] for b in self.get_ancestors(parent_id) ]

        return branches

    def get_ancestor_set(self, term_id, rels=_allrels):
        """Set containing all the ancestors of term_id for the given rels.

        Args
        ----
        term_id: GO term
        rels: a list of GO relationships: is_a, part_of, etc.

        Output
        ------
        A python set containing ancestors.
        """
        ancestors = self.get_ancestors(term_id, rels)
        ancestors = [set(a) for a in ancestors]

        return set.union(*ancestors)

    def get_namespace_terms(self, namespace):
        terms = set()
        for go_id, obj in self.ont.items():
            if obj['namespace'] == namespace:
                terms.add(go_id)
        return terms

    def get_parents(self, term_id):
        return set(self.ont[term_id]['is_a']) | \
            set(self.ont[term_id]['part_of']) | \
            set(self.ont[term_id]['has_part']) | \
            set(self.ont[term_id]['regulates']) | \
            set(self.ont[term_id]['negatively_regulates']) | \
            set(self.ont[term_id]['positively_regulates']) | \
            set(self.ont[term_id]['occurs_in']) | \
            set(self.ont[term_id]['ends_during']) | \
            set(self.ont[term_id]['happens_during'])
#
def read(obo_path,
         with_rels=False,
         remove_obs=False,
         include_alt_ids=False):
    """
    Args
    ----

    obo_path:   path to OBO file
    with_rels:  includes non-is-a GO relationships
    remove_obs: remove obsolete terms
    include_alt_ids: include alternative ids as valid GO terms
    """
    go = Ontology(obo_path,
                  with_rels=with_rels,
                  remove_obs=remove_obs,
                  include_alt_ids=include_alt_ids)

    return go
