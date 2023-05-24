import click

from .proper_gator import clone as clone_


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--only-tags",
    default=None,
    help="Tags from the target container to be the only tags included in the cloning "
    "process. Format names of tags separated with commas.",
)
@click.option(
    "--only-triggers",
    default=None,
    help="Triggers from the target container to be the only triggers included in the "
    "cloning process. Format names of triggers separated with commas.",
)
@click.option(
    "--only-variables",
    default=None,
    help="Variables from the target container to be the only variables included in the "
    "cloning process. Format names of variables separated with commas.",
)
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
    "--include-containers",
    default=None,
    help="The only containers to include for the cloning process."
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
    default="BioPharma Dive",
    show_default=True,
    help="The container to clone from",
)
def clone(target_container, target_workspace, exclude_containers, include_containers, exclude_variables,
          exclude_triggers, exclude_tags, only_variables, only_triggers, only_tags):
    """
    Clone tags from the target container to other containers in the same account
    """

    def split_and_trim(str):
        return [s.strip() for s in str.split(",")]

    if exclude_containers:
        exclude_containers = split_and_trim(exclude_containers)
    if include_containers:
        include_containers = split_and_trim(include_containers)
    if exclude_variables:
        exclude_variables = split_and_trim(exclude_variables)
    if exclude_triggers:
        exclude_triggers = split_and_trim(exclude_triggers)
    if exclude_tags:
        exclude_tags = split_and_trim(exclude_tags)
    if only_variables:
        only_variables = split_and_trim(only_variables)
    if only_triggers:
        only_triggers = split_and_trim(only_triggers)
    if only_tags:
        only_tags = split_and_trim(only_tags)

    clone_(
        target_container,
        target_workspace,
        exclude_containers,
        include_containers,
        exclude_variables,
        exclude_triggers,
        exclude_tags,
        only_variables,
        only_triggers,
        only_tags,
    )
