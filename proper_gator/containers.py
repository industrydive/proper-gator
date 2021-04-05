from proper_gator.service import execute


def get_containers(service, account_id):
    """Get all containers for a given account

    :param service: The Google service object
    :type service: Resource
    :param account_id: Account ID found in settings
    :type account_id: str
    :return: A collection of containers in the Google Tag Manager List Response format
    :rtype: dict
    """
    account_path = f"accounts/{account_id}"
    containers = execute(service.accounts().containers().list(parent=account_path))
    return containers


def find_target_container(container_wrapper, container_name):
    """Search through a collection of containers and return the container
    with the given name

    :param container_wrapper: A collection of containers in the Google Tag Manager
                              List Response format
    :type container_wrapper: dict
    :param container_name: The name of a container to find
    :type container_name: str
    :return: A Google Tag Manager containers
    :rtype: dict
    """
    for container in container_wrapper["container"]:
        if container["name"] == container_name:
            return container
    return None


def find_destination_containers(
    container_wrapper, target_container, exclude_containers=None
):
    """Search through a collection of containers and return all containers
    other than the given container

    :param container_wrapper: A collection of containers in the Google Tag Manager
                              List Response format
    :type container_wrapper: dict
    :param target_container: The target container, which will be excluded from the
                             returned list
    :type target_container: dict
    :param exclude_containers: A list of containers to exclude from being cloned to
    :type exclude_containers: list
    :return: A list of Google Tag Manager container objects
    :rtype: list
    """
    if not exclude_containers:
        exclude_containers = []
    destination_containers = []
    for container in container_wrapper["container"]:
        if (
            not container["containerId"] == target_container["containerId"]
            and container["name"] not in exclude_containers
        ):
            destination_containers.append(container)
    return destination_containers
