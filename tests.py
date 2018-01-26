import main

teststrings = {
    'Discard would have actually saved him from overdrawing since he would have less cards in his hand.': ['cards'],
    'less items': ['items'],
    'I have less water.': [],
    'the less we try': [],
    '>less items in a quote\n\nfoo': [],
    '>less items in a quote\n\nless items': ['items'],
    'bit of a less obvious case': [],
    'less metals less steels': ['metals', 'steels'],
    'it more or less negates the effects': [],
}

for key, value in teststrings.items():
    print("Test %s" % key)
    x = list(main.get_mistakes(key))
    print x, 'vs', value
    assert x == value
