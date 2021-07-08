#!/usr/bin/env python
"""
Include and compare BOTH choices for loader implementation in `ansible.parsing.yaml.loader`
"""

from yaml.composer import Composer
from yaml.reader import Reader
from yaml.scanner import Scanner
from yaml.parser import Parser
from yaml.resolver import Resolver

try:
    from yaml import CParser
except ImportError:
    try:
        from _yaml import CParser
    except ImportError:
        try:
            from yaml._yaml import CParser
        except ImportError:
            try:
                from yaml.cyaml import CParser
            except ImportError:
                print('Could not find a CParser implementation. \
                       The CParser bug cannot be demonstrated.')
                raise SystemExit


from ansible.parsing.yaml.constructor import AnsibleConstructor


class AnsibleCLoader(CParser, AnsibleConstructor, Resolver):
    def __init__(self, stream, file_name=None, vault_secrets=None):
        CParser.__init__(self, stream)
        AnsibleConstructor.__init__(self, file_name=file_name, vault_secrets=vault_secrets)
        Resolver.__init__(self)


class AnsiblePyLoader(Reader, Scanner, Parser, Composer, AnsibleConstructor, Resolver):
    def __init__(self, stream, file_name=None, vault_secrets=None):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        AnsibleConstructor.__init__(self, file_name=file_name, vault_secrets=vault_secrets)
        Resolver.__init__(self)


if __name__ == '__main__':
    from sys import argv
    from json import dumps

    def validate(loader_class, filename):
        print('\x1b[1;33m', loader_class, filename, '\x1b[m')
        try:
            with open(filename, 'rb') as stream:
                data = loader_class(stream).get_single_data()
                print(dumps(data, indent=2))
        except Exception as exception:
            print('\x1b[1;31m', exception, '\x1b[m')

    for filename in argv[1:]:
        validate(AnsibleCLoader, filename)
        validate(AnsiblePyLoader, filename)
