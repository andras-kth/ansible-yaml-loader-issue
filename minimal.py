from yaml import load, CLoader, Loader

def test(string):
    print('\x1b[7m# Original input\x1b[27m')
    print(string)
    print('\x1b[1m# Parsed (libyaml)\x1b[m')
    try:
        print(load(string, Loader=CLoader))
    except Exception as exception:
        print('\x1b[1;31m' + str(exception) + '\x1b[m')
    data = load(string, Loader=Loader)
    print('\x1b[1m# Parsed (pyyaml)\x1b[m')
    print(data)
    return data

# quoted string == literal block
assert test('key: "\\tvalue\\n"') == test('key: |\n  \tvalue\n')
