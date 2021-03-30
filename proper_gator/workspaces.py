from proper_gator.service import execute


def get_workspaces(service, container):
    workspaces = execute(
        service.accounts().containers().workspaces().list(parent=container["path"])
    )

    return workspaces


def find_workspace(workspace_wrapper, workspace_name):
    for workspace in workspace_wrapper["workspace"]:
        if workspace["name"] == workspace_name:
            return workspace
    return None


def get_destination_workspaces(service, destination_containers, workspace_name):
    destination_workspaces = []
    for container in destination_containers:
        workspaces = get_workspaces(service, container)
        workspace = find_workspace(workspaces, workspace_name)
        if workspace is None:
            workspace = create_workspace(service, container, workspace_name)
        destination_workspaces.append(workspace)
    return destination_workspaces


def create_workspace(service, container, workspace_name):
    workspace_body = {"name": workspace_name}
    workspace = (
        service.accounts()
        .containers()
        .workspaces()
        .create(parent=container["path"], body=workspace_body)
        .execute()
    )
    print(f"Created {workspace_name} in {container['name']}")
    return workspace
