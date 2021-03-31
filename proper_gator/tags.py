from proper_gator.service import execute


def get_tags(service, workspace):
    """Get all tags that exist in a given workspace

    https://googleapis.github.io/google-api-python-client/docs/dyn/tagmanager_v2.accounts.containers.workspaces.tags.html#list

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param workspace: A Google Tag Manager workspace
    :type workspace: dict
    :return: A collection of tags in the Google Tag Manager List Response format
    :rtype: dict
    """
    tags = execute(
        service.accounts()
        .containers()
        .workspaces()
        .tags()
        .list(parent=workspace["path"])
    )

    return tags


def create_tag(service, workspace, tag_body):
    """Create a tag in a given workspace

    https://googleapis.github.io/google-api-python-client/docs/dyn/tagmanager_v2.accounts.containers.workspaces.tags.html#create

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param workspace: A Google Tag Manager workspace
    :type workspace: dict
    :param tag_body: The request body that the tag should be created with
    :type tag_body: dict
    :return: The created tag
    :rtype: dict
    """
    new_tag = execute(
        service.accounts()
        .containers()
        .workspaces()
        .tags()
        .create(parent=workspace["path"], body=tag_body)
    )
    print(
        f"Created {tag_body['name']} in "
        f"{workspace['name']} - {workspace['containerId']}"
    )
    return new_tag


def clone_tags(
    service, target_workspace, destination_workspace, trigger_mapping, variable_mapping
):
    """For each tag in the target_workspace, create a tag in each of the
    destination workspaces.

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param target_workspace: The Google Tag Manager workspace to clone tags from
    :type target_workspace: dict
    :param destination_workspace: A Google Tag Manager workspace to clone tags to
    :type destination_workspace: dict
    :param trigger_mapping: A mapping of the triggers that exist on the target
                            workspace to the destination workspace
    :type trigger_mapping: dict
    :param variable_mapping: A mapping of the variables that exist on the target
                            workspace to the destination workspace
    :type variable_mapping: dict
    """
    tags_wrapper = get_tags(service, target_workspace)
    for tag in tags_wrapper["tag"]:
        tag_body = create_tag_body(tag, trigger_mapping)
        create_tag(service, destination_workspace, tag_body)


def create_tag_body(tag, trigger_mapping):
    """Given a tag, remove all keys that are specific to that tag
    and return keys + values that can be used to clone another tag

    https://googleapis.github.io/google-api-python-client/docs/dyn/tagmanager_v2.accounts.containers.workspaces.tags.html#create

    :param tag: The tag to convert into a request body
    :type tag: dict
    :param trigger_mapping: A mapping of the triggers that exist on the target
                            workspace to the destination workspace
    :type trigger_mapping: dict
    :return: A request body to be used in the create tag method
    :rtype: dict
    """
    body = {}
    non_mutable_keys = [
        "accountId",
        "containerId",
        "fingerprint",
        "parentFolderId",
        "path",
        "tagManagerUrl",
        "tagId",
        "workspaceId",
    ]

    for k, v in tag.items():
        if k not in non_mutable_keys:
            if "TriggerId" not in k:
                body[k] = v
            else:
                mapped_triggers = []
                for i in v:
                    mapped_triggers = trigger_mapping[i]
                body[k] = mapped_triggers
    return body
