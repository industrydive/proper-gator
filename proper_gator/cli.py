import click

from .proper_gator import clone as clone_


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--exclude-tags",
    default=None,
    help="Tags from the target container to exclude from the cloning process. "
    "Format names of tags separated with commas.",
)
@click.option(
    "--exclude-triggers",
    default=None,
    help="Triggers from the target container to exclude from the cloning process."
    "Format names of triggers separated with commas.",
)
@click.option(
    "--exclude-variables",
    default=None,
    help="Variables from the target container to exclude from the cloning process."
    "Format names of variables separated with commas.",
)
@click.option(
    "--exclude-containers",
    default=None,
    help="Containers to exclude from the cloning process."
    "Format names of containers separated with commas.",
)
@click.option(
    "--target-workspace",
    default="proper_gator_staging",
    show_default=True,
    help="The workspace to clone from",
)
@click.option(
    "--target-container",
    default="Biopharma Dive",
    show_default=True,
    help="The container to clone from",
)
def clone(
    target_container,
    target_workspace,
    exclude_containers,
    exclude_variables,
    exclude_triggers,
    exclude_tags,
):
    """
    Clone tags from the target container to other containers in the same account
    """
    if exclude_containers:
        exclude_containers = exclude_containers.split(",")
    if exclude_variables:
        exclude_variables = exclude_variables.split(",")
    if exclude_triggers:
        exclude_triggers = exclude_triggers.split(",")
    if exclude_tags:
        exclude_tags = exclude_tags.split(",")

    clone_(
        target_container,
        target_workspace,
        exclude_containers,
        exclude_variables,
        exclude_triggers,
        exclude_tags,
    )
