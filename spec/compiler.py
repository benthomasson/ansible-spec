#!/usr/bin/python
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
import os
import sys
import textwrap
import logging

from StringIO import StringIO

import yaml

logger = logging.getLogger(__name__)
output = StringIO()

SECTIONS = ['shebang', 'license', 'metadata', 'documentation', 'example',
            'return', 'imports', 'body']

def add(line, spaces=0):
    line = line.rjust(len(line)+spaces, ' ')
    output.write(line + '\n')

def do_shebang(spec, args):
    add('#!/usr/bin/python')

def do_license(spec, args):
    license = """#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
"""
    add(license)

def do_metadata(spec, args):
    # write ansible metadata
    if 'ansible_metadata' not in spec:
        logging.error('missing required element ansible_metadata')
        sys.exit(1)
    metadata = spec['ansible_metadata']
    add('ANSIBLE_METADATA = {')
    add("'status': %s," % metadata['status'], 4)
    add("'supported_by': '%s'," % metadata['supported_by'], 4)
    add("'version': '%s'" % metadata.get('version', '1.0'), 4)
    add("}\n")

def do_documentation(spec, args):
    # write documentation
    add('DOCUMENTATION = """')
    add('---')
    add('module: %s' % spec['module_name'])

    if args.version_added:
        add('version_added: "%s"' % args.version_added)

    if args.author:
        add('author: "%s"' % args.author)

    add('short_description: %s' % spec['short_description'])

    add('description:')
    description = spec['description'][0]
    lines = textwrap.wrap(description, 70)
    for index, line in enumerate(lines):
        if index == 0:
            line = '- %s' % line
            add(line, 2)
        else:
            add(line, 4)

    if 'extends_documentation_fragment' in spec:
        add('extends_documentation_fragment: %s' % spec['extends_documentation_fragment'])

    add('options:')

    for key, value in spec['options'].items():
        add("%s:" % key, 2)

        add("description:", 4)
        description = value['description'][0]
        lines = textwrap.wrap(description, 70)
        for index, line in enumerate(lines):
            if index == 0:
                line = '- %s' % line
                add(line, 6)
            else:
                add(line, 8)

        if value.get('required') is True:
            add("required: true", 4)
            if 'default' not in value:
                logging.error('default value is required when required=true')
                sys.exit(1)

        if 'default' in value:
            if value['default'] in (True, False):
                val = str(value['default']).lower()
            elif value['default'] is None:
                val = 'null'
            else:
                val = str(value['default'])
            add('default: %s' % val, 4)

        if 'choices' in value:
            add('choices:', 4)
            for item in value['choices']:
                add('- %s' % item, 6)

        if 'aliases' in value:
            add('aliases:', 4)
            for item in value['aliases']:
                add('- %s' % item, 6)

        if 'version_added' in value:
            add("version_added: '%s'" % value['version_added'], 4)

    if spec['requirements']:
        add('requirements:')
        for item in spec['requirements']:
            add('- %s' % item, 2)

    if spec['notes']:
        add('notes:')
        for item in spec['notes']:
            add('- %s' % item, 2)

    add('"""')

def do_example(spec, args):
    # write EXAMPLES
    if 'examples' not in spec:
        logging.error('missing required section EXAMPLE')
        sys.exit(1)
    elif not isinstance(spec['examples'], basestring):
        logging.error('invalid value for examples, expected string, got %s' % type(spec['examples']))
        sys.exit(1)

    add('')
    add('EXAMPLES = """')
    add(str(spec['examples']).strip())
    add('"""')

def do_return(spec, args):
    # write RETURN
    if 'return' not in spec:
        logging.error('missing required section RETURN')
        sys.exit(1)
    elif not isinstance(spec['return'], basestring):
        logging.error('invalid value for return, expected string, got %s' % type(spec['return']))
        sys.exit(1)

    add('')
    add('RETURN = """')
    add(str(spec['return']).strip())
    add('"""')

def do_imports(spec, args):
    add('from ansible.module_utils.basic import AnsibleModule')

def do_body(spec, args):
    #write body
    add('')
    add('def main():')
    add('"""main entry point for module execution', 4)
    add('"""', 4)
    add('argument_spec = dict(', 4)

    options_len = len(spec['options'].items())
    for index, (key, value) in enumerate(spec['options'].items()):
        line = '%s=dict(' % key

        if 'type' in value:
            # skip str as its the default
            if value['type'] != 'str':
                line += "type='%s'" % value['type']

        if 'default' in value:
            if value['default'] != None:
                if value.get('type') == 'bool':
                    if value['default'] is True:
                        line += ", default=True"
                    elif value['default'] is False:
                        line += ", default=False"
                    else:
                        raise ValueError('invalid value for bool')
                else:
                    line += ", default='%s'" % value['default']

        if 'choices' in value:
            if value.get('type') != 'bool':
                line += ", choices=%s" % value['choices']

        if 'aliases' in value:
            line += ", aliases=%s" % value['aliases']

        if 'no_log' in value:
            if value['no_log'] is True:
                line += ", default=True"
            elif value['default'] is False:
                line += ", default=False"
            else:
                raise ValueError('invalid value for bool')

        line = line.replace('(, ', '(')

        line += ')'
        if index != options_len-1:
            line += ','
        add(line, 8)

    add(')', 4)

    add('')
    add('module = AnsibleModule(argument_spec=argument_spec,', 4)
    add('supports_check_mode=%s)' % spec.get('supports_check_mode', False), 27)

    add('')
    add("module.fail_json(msg='not implemented')", 4)

    add('')
    add('if __name__ == "__main__":')
    add('main()', 4)


def run(args):

    if not os.path.exists(args.spec):
        logging.error('spec file not found')

    spec = yaml.load(open(args.spec))

    for name in SECTIONS:
        func = globals().get('do_%s' % name)
        func(spec, args)

    contents = output.getvalue()

    if args.output:
        open(args.output, 'w').write(contents)
    else:
        sys.stdout.write(contents)





