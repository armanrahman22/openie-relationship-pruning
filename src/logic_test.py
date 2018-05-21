from logic import prune, dict_to_relation

"""
Barack Obama was born in Hawaii.
"""
relation_1 = {'subject': 'Barack Obama', 'relation': 'was', 'argument': 'born'}
relation_2 = {'subject': 'Barack Obama', 'relation': 'born in', 'argument': 'Hawaii'}

"""
[Mrs. Dalloway] felt the perpetual sense, as she watched the taxi cabs, of being out, out, far out to sea and alone; 
[Mrs. Dalloway] always felt that it was very, very, dangerous to live even one day.
"""
relation_3 = {'subject': 'Mrs. Dalloway', 'relation': 'felt', 'argument': 'the perpetual sense as she watched the taxi cabs of being out'}
relation_4 = {'subject': 'Mrs. Dalloway', 'relation': 'felt', 'argument': 'the perpetual sense alone'}
relation_5 = {'subject': 'Mrs. Dalloway', 'relation': 'watched', 'argument': 'the taxi cabs of being out'}
relation_6 = {'subject': 'Mrs. Dalloway', 'relation': 'felt', 'argument': 'that it was very very dangerous to live even one day always'}
relation_7 = {'subject': 'it', 'relation': 'was', 'argument': 'very very dangerous to live even one day'}


"""
Human speech [sounds] like a cracked kettle on which we tap crude rhythms for bears to dance to,
while we long to make music that will melt the stars.
"""
relation_8 = {'subject': 'Human speech', 'relation': 'sounds', 'argument': 'like a cracked kettle while we long to make music'}
relation_9 = {'subject': 'Human speech', 'relation': 'sounds', 'argument': 'like a cracked kettle'}
relation_10 = {'subject': 'We', 'relation': 'make', 'argument': 'music'}
relation_11 = {'subject': 'Humans', 'relation': 'tap', 'argument': 'crude rhythms for bears to dance to on a cracked kettle'}
relation_12 = {'subject': 'Humans', 'relation': 'tap', 'argument': 'crude rhythms for bears to dance to'}
relation_13 = {'subject': 'Humans', 'relation': 'tap', 'argument': 'crude rhythms for bears'}
relation_14 = {'subject': 'music', 'relation': 'will melt', 'argument': 'the stars'}
relation_15 = {'subject': 'music', 'relation': 'melt', 'argument': 'the stars'}


relations_small = [relation_1, relation_2]
relations_medium = [relation_3, relation_4, relation_5, relation_6, relation_7]
relations_large = [relation_8, relation_9, relation_10, relation_11, relation_12, relation_13, relation_14, relation_15]


def test_prune_small():
    pruned = prune(relations_small)
    assert len(pruned) == 1
    assert dict_to_relation(relation_2) in pruned


def test_prune_medium():
    pruned = prune(relations_medium)
    assert len(pruned) == 3
    assert dict_to_relation(relation_3) in pruned
    assert dict_to_relation(relation_5) in pruned
    assert dict_to_relation(relation_6) in pruned


def test_prune_large():
    pruned = prune(relations_large)
    assert len(pruned) == 3
    assert dict_to_relation(relation_8) in pruned
    assert dict_to_relation(relation_11) in pruned
    assert dict_to_relation(relation_14) in pruned

test_prune_small()