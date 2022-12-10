"""
Commands for managing transfers on Put.IO.
"""

import click
import yaml

from putio_automator.cli import cli


@cli.group()
def transfers():
    pass


@transfers.command()
@click.pass_context
@click.option('--statuses', help='Comma-separated list of statuses to be cancelled')
def cancel_by_status(ctx, statuses):
    "Cancel transfers by status"

    if isinstance(statuses, str):
        statuses = statuses.split(',')

    transfer_ids = []
    for transfer in ctx.obj['CLIENT'].Transfer.list():
        if transfer.status in statuses:
            transfer_ids.append(transfer.id)

    if len(transfer_ids):
        ctx.obj['CLIENT'].Transfer.cancel_multi(transfer_ids)


@transfers.command()
@click.pass_context
def cancel_completed(ctx):
    "Cancel completed transfers"
    ctx.invoke(cancel_by_status, 'COMPLETED')


@transfers.command()
@click.pass_context
def cancel_seeding(ctx):
    "Cancel seeding transfers"
    ctx.invoke(cancel_by_status, 'SEEDING')


@transfers.command()
@click.pass_context
def clean(ctx):
    "Clean finished transfers"
    ctx.obj['CLIENT'].Transfer.clean()


@transfers.command()
@click.pass_context
def groom(ctx):
    "Cancel seeding and completed transfers, and clean afterwards"
    ctx.invoke(cancel_by_status, statuses=['SEEDING', 'COMPLETED'])
    ctx.invoke(clean)


@transfers.command()
@click.pass_context
def list(ctx):
    "List transfers"
    transfers = ctx.obj['CLIENT'].Transfer.list()
    click.echo(yaml.dump([vars(t) for t in transfers]))
