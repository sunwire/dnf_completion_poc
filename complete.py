#!/usr/bin/env python3
import sys
import os
import importlib


COMM = 0
SUB_COMM = 1

CUR = 2
PREV = 3

all_commands = [
    'alias', 'autoremove', 'check', 'check-update', 'clean', 'deplist',
    'distro-sync', 'downgrade', 'group', 'help', 'history', 'info', 'install',
    'list', 'makecache', 'mark', 'module', 'provides', 'reinstall', 'remove',
    'repolist', 'repoquery', 'repository-packages', 'search', 'shell', 'swap',
    'updateinfo', 'upgrade', 'upgrade-minimal'
]

argv = sys.argv


def sub_commands(args, command, commands):
    if args[PREV] == command:
        for comm in commands:
            if comm.find(args[CUR]) == 0:
                print(comm)
        exit()


""" Ignore all files not end with .py and start with __ """
def ignore(fn):
    if not fn.startswith('__') and fn.endswith('.py'):
        return True
    return False


""" plugins section """
os.environ['PYTHON_EGG_CACHE'] = '/tmp'
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

files = os.listdir(os.path.dirname(os.path.abspath(__file__)) + '/plugins')
plugins = [file[:-3] for file in files if ignore(file)]
for plugin in plugins:
    plug = importlib.import_module('plugins.' + plugin)
#    all_commands.extend(plug.commands)
    for command in plug.commands:
        all_commands.append(command[COMM])
        sub_commands(argv, command[COMM], command[SUB_COMM])

""" autocompletion sub commands """
sub_commands(argv, 'autoremove', ())
sub_commands(argv, 'help', ())
sub_commands(argv, 'shell', ())
sub_commands(argv, 'search', ('--all'))
sub_commands(argv, 'alias', ('list', 'add', 'delete'))
sub_commands(
    argv, 'check',
    ('--all', '--dependencies', '--duplicates', '--obsoleted', '--provides'))
sub_commands(argv, 'history',
             ('info', 'list', 'redo', 'rollback', 'undo', 'userinstalled'))


""" autocompletion commands """
if argv[CUR] == '' and argv[PREV] == argv[1]:
    for comm in all_commands:
        print(comm)
elif argv[CUR] != '':
    for comm in all_commands:
        if comm.find(argv[CUR]) == 0:
            print(comm)

#print(args)
