from proper_gator.service import execute


def get_containers(service, account_id):
    """Get all containers for a given account

    :param service: The Google service object
    :type service: Resource
    :param account_id: Account ID found
    :type account_id: [type]
    :return: [description]
    :rtype: [type]
    """
    account_path = f"accounts/{account_id}"
    containers = execute(service.accounts().containers().list(parent=account_path))
    return containers


def find_target_container(container_wrapper, container_name):
    """
    Given a list of containers, return the container with the given name

    """
    for container in container_wrapper["container"]:
        if container["name"] == container_name:
            return container
    return None


def find_destination_containers(container_wrapper, target_container):
    destination_containers = []
    for container in container_wrapper["container"]:
        if not container["containerId"] == target_container["containerId"]:
            destination_containers.append(container)
    return destination_containers
