from proper_gator.service import execute


def get_tags(service, workspace):
    tags = execute(
        service.accounts()
        .containers()
        .workspaces()
        .tags()
        .list(parent=workspace["path"])
    )

    return tags


def create_tag(service, workspace, tag_body):
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
    destination workspaces. If

    :param service: [description]
    :type service: [type]
    :param target_workspace: [description]
    :type target_workspace: [type]
    :param destination_workspaces: [description]
    :type destination_workspaces: [type]
    """
    tags_wrapper = get_tags(service, target_workspace)
    for tag in tags_wrapper["tag"]:
        tag_body = create_tag_body(tag, trigger_mapping)
        create_tag(service, destination_workspace, tag_body)


def create_tag_body(tag, trigger_mapping):
    """Given a tag, remove all keys that are specific to that tag
    and return keys + values that can be used to clone another tag

    https://googleapis.github.io/google-api-python-client/docs/dyn/tagmanager_v2.accounts.containers.workspaces.tags.html#create

    :param tag: [description]
    :type tag: [type]
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
