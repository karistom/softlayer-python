"""List number of block storage volumes limit per datacenter."""
# :license: MIT, see LICENSE for more details.

import click
import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting

DEFAULT_COLUMNS = [
    'Datacenter',
    'MaximumAvailableCount',
    'ProvisionedCount'
]


@click.command(cls=SoftLayer.CLI.command.SLCommand, )
@click.option('--sortby', help='Column to sort by', default='Datacenter')
@click.option('--datacenter', '-d', help='Filter by datacenter')
@environment.pass_env
def cli(env, sortby, datacenter):
    """List number of block storage volumes limit per datacenter.

    EXAMPLE::
        slcli block volume-limits
        This command lists the storage limits per datacenter for this account.
"""

    block_manager = SoftLayer.BlockStorageManager(env.client)
    block_volumes = block_manager.list_block_volume_limit()

    table = formatting.KeyValueTable(DEFAULT_COLUMNS)
    table.sortby = sortby

    for volumen in block_volumes:
        if datacenter:
            if volumen.get('datacenterName') != '':
                if volumen.get('datacenterName') == datacenter:
                    table.add_row([volumen.get('datacenterName'),
                                   volumen.get('maximumAvailableCount'),
                                   volumen.get('provisionedCount')])
                    break
        else:
            if volumen.get('datacenterName') != '':
                table.add_row([volumen.get('datacenterName'), volumen.get('maximumAvailableCount'),
                               volumen.get('provisionedCount')])
            else:
                table.add_row([' - ',
                               volumen.get('maximumAvailableCount'),
                               volumen.get('provisionedCount')])
    env.fout(table)
