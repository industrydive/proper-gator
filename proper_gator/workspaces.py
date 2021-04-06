from proper_gator.service import execute


def get_workspaces(service, container):
    """Get all workspaces in a given container

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param container: A Google Tag Manager container
    :type container: dict
    :return: A collection of workspaces in the Google Tag Manager List Response format
    :rtype: dict
    """
    workspaces = execute(
        service.accounts().containers().workspaces().list(parent=container["path"])
    )

    return workspaces


def create_workspace(service, container, workspace_name):
    """Create a workspace with the given name in a given container

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param container: A Google Tag Manager container
    :type container: dict
    :param workspace_name: The name of a workspace to create
    :type workspace_name: str
    :return: A Google Tag Manager workspace
    :rtype: dict
    """
    workspace_body = {"name": workspace_name}
    workspace = execute(
        service.accounts()
        .containers()
        .workspaces()
        .create(parent=container["path"], body=workspace_body)
    )
    print(f"Created {workspace_name} in {container['name']}")
    return workspace


def find_workspace(workspace_wrapper, workspace_name):
    """Search through a collection of workspaces and return the workspace
    with the given name

    :param workspace_wrapper: A collection of workspaces in the Google Tag Manager
                              List Response format
    :type workspace_wrapper: dict
    :param workspace_name: The name of a workspace to find
    :type workspace_name: str
    :return: A Google Tag Manager workspace
    :rtype: dict
    """
    if "workspace" in workspace_wrapper:
        for workspace in workspace_wrapper["workspace"]:
            if workspace["name"] == workspace_name:
                return workspace
    return None


def get_destination_workspaces(service, destination_containers, workspace_name):
    """Given a collection of containers, find or create a workspace with the
    given name

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param destination_containers: A list of Google Tag Manager container objects
    :type destination_containers: list
    :param workspace_name: The name of the workspace to find or create
    :type workspace_name: str
    :return: A list of Google Tag Manager workspace objects
    :rtype: list
    """
    destination_workspaces = []
    for container in destination_containers:
        workspaces = get_workspaces(service, container)
        workspace = find_workspace(workspaces, workspace_name)
        if workspace is None:
            workspace = create_workspace(service, container, workspace_name)
        destination_workspaces.append(workspace)
    return destination_workspaces
