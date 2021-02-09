#!/usr/bin/env python3

import click
from .medium import barcodecheck

@click.command()
def cli():
    """Example script."""
    click.echo('Hello World!')