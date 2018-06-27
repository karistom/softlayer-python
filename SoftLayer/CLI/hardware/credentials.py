"""List server credentials."""
# :license: MIT, see LICENSE for more details.

import click

import SoftLayer
from SoftLayer import exceptions
from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting
from SoftLayer.CLI import helpers


@click.command()
@click.argument('identifier')
@environment.pass_env
def cli(env, identifier):
    """List server credentials."""

    manager = SoftLayer.HardwareManager(env.client)
    hardware_id = helpers.resolve_id(manager.resolve_ids,
                                     identifier,
                                     'hardware')
    instance = manager.get_hardware(hardware_id)

    table = formatting.Table(['username', 'password'])
    if 'passwords' not in instance['operatingSystem']:
        raise exceptions.SoftLayerError("No passwords found in operatingSystem")

    for item in instance['operatingSystem']['passwords']:
        if 'password' not in item:
            raise exceptions.SoftLayerError("No password found in operatingSystem passwords")
        else:
            table.add_row([item['username'], item['password']])
    env.fout(table)
