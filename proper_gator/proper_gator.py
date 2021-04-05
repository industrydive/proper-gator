from proper_gator.authentication import get_credentials
from proper_gator.containers import (
    find_destination_containers,
    find_target_container,
    get_containers,
)
from proper_gator.service import get_service
from proper_gator.tags import clone_tags
from proper_gator.triggers import clone_triggers
from proper_gator.variables import clone_variables
from proper_gator.workspaces import (
    find_workspace,
    get_destination_workspaces,
    get_workspaces,
)
from settings import ACCOUNT_ID

# TODO: Abstract out finding a arbitrary resource supporting pagination
# def find_target_resource(resource_wrapper, resource_type, target_name):
#     while resource_wrapper["nextPageToken"]:
#         for resource in resource_wrapper[resource_type]:
#             if resource["name"] == target_name:
#                 return resource


def clone(
    container_name="Biopharma Dive",
    workspace_name="proper_gator_staging",
    exclude_containers=None,
    exclude_variables=None,
    exclude_triggers=None,
    exclude_tags=None,
):
    credentials = get_credentials()
    service = get_service(credentials)

    containers = get_containers(service, ACCOUNT_ID)
    target_container = find_target_container(containers, container_name)
    destination_containers = find_destination_containers(
        containers, target_container, exclude_containers
    )

    target_container_workspaces = get_workspaces(service, target_container)
    target_workspace = find_workspace(target_container_workspaces, workspace_name)
    destination_workspaces = get_destination_workspaces(
        service, destination_containers, workspace_name
    )

    for destination_workspace in destination_workspaces:
        variable_mapping = clone_variables(
            service, target_workspace, destination_workspace, exclude_variables
        )
        trigger_mapping = clone_triggers(
            service, target_workspace, destination_workspace, exclude_triggers
        )
        clone_tags(
            service,
            target_workspace,
            destination_workspace,
            trigger_mapping,
            variable_mapping,
            exclude_tags,
        )
