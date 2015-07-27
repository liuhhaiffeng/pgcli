# -*- coding: utf-8 -*-
"""
Steps for behavioral style tests are defined in this module.
Each step is defined by the string decorating it.
This string is used to call the step in "*.feature" file.
"""
from __future__ import unicode_literals

import pip
import pexpect

from behave import given, when, then


@given('we have pgcli installed')
def step_install_cli(_):
    """
    Check that pgcli is in installed modules.
    """
    dists = set([di.key for di in pip.get_installed_distributions()])
    assert 'pgcli' in dists


@when('we run pgcli')
def step_run_cli(context):
    """
    Run the process using pexpect.
    """
    context.cli = pexpect.spawnu('pgcli')


@when('we wait for prompt')
def step_wait_prompt(context):
    """
    Make sure prompt is displayed.
    """
    context.cli.expect('{0}> '.format(context.conf['dbname']))


@when('we send "ctrl + d"')
def step_ctrl_d(context):
    """
    Send Ctrl + D to hopefully exit.
    """
    context.cli.sendcontrol('d')
    context.exit_sent = True


@when('we send "\?" command')
def step_send_help(context):
    """
    Send \? to see help.
    """
    context.cli.sendline('\?')


@when('we send "create database" command')
def step_db_create(context):
    """
    Send create database.
    """
    context.cli.sendline('create database pgcli_behave_tmp;')
    context.response = {
        'database_name': 'pgcli_behave_tmp'
    }


@when('we send "drop database" command')
def step_db_drop(context):
    """
    Send drop database.
    """
    context.cli.sendline('drop database pgcli_behave_tmp;')


@when('we connect to test database')
def step_db_connect_test(context):
    """
    Send connect to database.
    """
    db_name = context.config.userdata.get('pg_test_db', None)
    context.cli.sendline('\connect {0}'.format(db_name))


@when('we connect to postgres')
def step_db_connect_postgres(context):
    """
    Send connect to database.
    """
    context.cli.sendline('\connect postgres')


@then('pgcli exits')
def step_wait_exit(context):
    """
    Make sure the cli exits.
    """
    context.cli.expect(pexpect.EOF)


@then('we see pgcli prompt')
def step_see_prompt(context):
    """
    Wait to see the prompt.
    """
    context.cli.expect('{0}> '.format(context.conf['dbname']))


@then('we see help output')
def step_see_help(context):
    for expected_line in context.fixture_data['help_commands.txt']:
        try:
            context.cli.expect_exact(expected_line, timeout=1)
        except Exception:
            raise Exception('Expected: ' + expected_line.strip() + '!')


@then('we see database created')
def step_see_db_created(context):
    """
    Wait to see create database output.
    """
    context.cli.expect_exact('CREATE DATABASE', timeout=2)


@then('we see database dropped')
def step_see_db_dropped(context):
    """
    Wait to see drop database output.
    """
    context.cli.expect_exact('DROP DATABASE', timeout=2)


@then('we see database connected')
def step_see_db_connected(context):
    """
    Wait to see drop database output.
    """
    context.cli.expect_exact('You are now connected to database', timeout=2)
