# ansible-yaml-loader-issue
Demonstrate inconsistent behavior for `ansible.parsing.yaml.loader.AnsibleLoader`

https://github.com/ansible/ansible/issues/75212

Two equivalent ways to specifiy the same content:
```
user@host:~/ansible-yaml-loader-issue$ diff roles/*/tasks/main.yml
```
```diff
8,10c8
<     block: |
<       	extra line with leading TAB;
<       	another line with leading TAB;
---
>     block: "\textra line with leading TAB;\n\tanother line with leading TAB;\n"
```

Different behaviour when running with or without `libyaml` / `CParser`:
```console
user@host:~/ansible-yaml-loader-issue$ ./loader.py roles/*/tasks/main.yml
 <class '__main__.AnsibleCLoader'> roles/easy_to_read/tasks/main.yml 
 while scanning a block scalar
  in "roles/easy_to_read/tasks/main.yml", line 8, column 12
found a tab character where an indentation space is expected
  in "roles/easy_to_read/tasks/main.yml", line 9, column 7 
 <class '__main__.AnsiblePyLoader'> roles/easy_to_read/tasks/main.yml 
[
  {
    "name": "Block-in-file with leading TAB",
    "blockinfile": {
      "path": "{{ test_conf }}",
      "insertbefore": "^};$",
      "marker": "\t// {mark} ANSIBLE MANAGED BLOCK",
      "block": "\textra line with leading TAB;\n\tanother line with leading TAB;\n"
    }
  }
]
 <class '__main__.AnsibleCLoader'> roles/hard_to_read/tasks/main.yml 
[
  {
    "name": "Block-in-file with leading TAB",
    "blockinfile": {
      "path": "{{ test_conf }}",
      "insertbefore": "^};$",
      "marker": "\t// {mark} ANSIBLE MANAGED BLOCK",
      "block": "\textra line with leading TAB;\n\tanother line with leading TAB;\n"
    }
  }
]
 <class '__main__.AnsiblePyLoader'> roles/hard_to_read/tasks/main.yml 
[
  {
    "name": "Block-in-file with leading TAB",
    "blockinfile": {
      "path": "{{ test_conf }}",
      "insertbefore": "^};$",
      "marker": "\t// {mark} ANSIBLE MANAGED BLOCK",
      "block": "\textra line with leading TAB;\n\tanother line with leading TAB;\n"
    }
  }
]
user@host:~/ansible-yaml-loader-issue$
````
