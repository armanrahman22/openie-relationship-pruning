from typing import Dict, List

from fuzzywuzzy import fuzz, process
from nltk.corpus import stopwords

import ujson as json
from env import MATCH_RATIO, MIN_ENTITY_LENGTH

STOP_WORDS = set(stopwords.words('english'))


class Relationship:
    def __init__(self, subject: str, relation: str, argument: str):
        self.subject = subject
        self.relation = relation
        self.argument = argument

    def to_dictionary(self):
        return {'subject': self.subject,
                'relation': self.relation,
                'argument': self.argument}

    def to_json(self):
        return json.dumps(self.to_dictionary())

    def __str__(self):
        return self.subject + " " + self.relation + " " + self.argument

    def __eq__(self, other):
        subject_eq = self.subject.lower == other.subject.lower
        relation_eq = self.relation.lower == other.relation.lower
        argument_eq = self.argument.lower == other.argument.lower
        return subject_eq and relation_eq and argument_eq


def prune(relation_dicts: List[Dict[str, str]]) -> List[Relationship]:
    """Main function that filters by domination and applies simple cleaning rules

    Arguments:
        relation_dicts {List[Dict[str, str]]} -- List containing
            dicts representing relations

    Returns:
        List[Relationship] -- List of relationships
    """
    relations = list(map(dict_to_relation, relation_dicts))
    relations = filter_domination(relations)
    relations = clean_simple_rules(relations)
    return relations


def dict_to_relation(relation: Dict[str, str]) -> Relationship:
    return Relationship(relation['subject'],
                        relation['relation'],
                        relation['argument'])


def filter_domination(relations: List[Relationship]) -> List[Relationship]:
    """This function filters out entites by domination theory. Only the
        entities with the most information are kept. For example:
            [(Virginia Woolf, pioneered, the use),
            (Virginia Woolf, pioneered, the use of stream),
            (Virginia Woolf, pioneered, the use of stream of consciousness)]
            -->
            [(Virginia Woolf, pioneered, the use of stream of consciousness)]

    Arguments:
        relations {List[Relationship]} -- relations to filter

    Returns:
        List[Relationship] -- filtered relations
    """

    relations_to_keep: List[Relationship] = []
    string_relations_dict: Dict[str, Relationship] = {}

    # Create a dictionary of relations as a string to Relationship
    for relation in relations:
        key = str(relation)
        string_relations_dict[key] = relation

    for i, relation in enumerate(relations):
        strings = string_relations_dict.keys()

        # get partial fuzzy matches rated by similarity to relation
        all_matches = process.extract(str(relation), strings,
                                      scorer=fuzz.partial_ratio)
        good_matches = [match[0] for match in all_matches
                        if match[1] > MATCH_RATIO]

        # get longest of the similar matches
        if len(good_matches):
            longest_relation = max(good_matches, key=len)
            relations_to_keep.append(string_relations_dict[longest_relation])
            rel = string_relations_dict[longest_relation].relation

        # Remove only relation tuples that have a similar relation
        # ie (Obama, born, Hawaii) and (Obama, born in, Honolulu Hawaii)
        for match in good_matches:
            match_rel = string_relations_dict[match].relation
            ratio = fuzz.partial_ratio(rel, match_rel)
            if ratio > MATCH_RATIO:
                string_relations_dict.pop(match, None)

        if len(string_relations_dict) == 0:
            break
    return relations_to_keep


def is_valid_relationship(relation: Relationship) -> bool:
    """Checks simple rules to clean spurious relationships

    Arguments:
        relation {Relationship} -- relationship to check

    Returns:
        bool -- true if it is a valid relationship
    """

    sub = relation.subject.lower()
    rel = relation.relation.lower()
    arg = relation.argument.lower()

    # discard circular relations
    if sub == rel or arg == sub:
        return False

    # discard relations with small entities
    if any(len(x) < MIN_ENTITY_LENGTH for x in (rel, sub, arg)):
        return False

    # discard stopword relations
    if any(x in STOP_WORDS for x in (rel, sub, arg)):
        return False

    return True


def clean_simple_rules(relations: List[Relationship]) -> List[Relationship]:
    return list(filter(is_valid_relationship, relations))
