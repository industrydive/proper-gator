from proper_gator.service import execute


def get_triggers(service, workspace):
    """Get all variables that exist in a given workspace

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param workspace: A Google Tag Manager workspace
    :type workspace: dict
    :return: A collection of triggers in the Google Tag Manager List Response format
    :rtype: dict
    """
    triggers = execute(
        service.accounts()
        .containers()
        .workspaces()
        .triggers()
        .list(parent=workspace["path"])
    )

    return triggers


def create_trigger(service, workspace, trigger_body):
    """Create a trigger in a given workspace

    https://googleapis.github.io/google-api-python-client/docs/dyn/tagmanager_v2.accounts.containers.workspaces.triggers.html#create

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param workspace: A Google Tag Manager workspace
    :type workspace: dict
    :param trigger_body: The request body that the trigger should be created with
    :type trigger_body: dict
    :return: The created trigger
    :rtype: dict
    """
    new_trigger = execute(
        service.accounts()
        .containers()
        .workspaces()
        .triggers()
        .create(parent=workspace["path"], body=trigger_body)
    )
    print(
        f"Created {trigger_body['name']} in "
        f"{workspace['name']} - {workspace['containerId']}"
    )
    return new_trigger


def clone_triggers(service, target_workspace, destination_workspace):
    """For each trigger in the target_workspace, create a trigger in each of the
    destination workspaces. If

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param target_workspace: The Google Tag Manager workspace to clone triggers from
    :type target_workspace: dict
    :param destination_workspace: A Google Tag Manager workspace to clone triggers to
    :type destination_workspace: dict
    :return: A mapping of the trigger ids from the target workspace to the trigger ids
             in the destination workspace.
    :rtype: dict
    """
    trigger_mapping = {}
    triggers_wrapper = get_triggers(service, target_workspace)
    for trigger in triggers_wrapper["trigger"]:
        trigger_body = create_trigger_body(trigger)
        new_trigger = create_trigger(service, destination_workspace, trigger_body)
        trigger_mapping[trigger["triggerId"]] = new_trigger["triggerId"]
    return trigger_mapping


def create_trigger_body(trigger):
    """Given a trigger, remove all keys that are specific to that trigger
    and return keys + values that can be used to clone another trigger

    https://googleapis.github.io/google-api-python-client/docs/dyn/tagmanager_v2.accounts.containers.workspaces.triggers.html#create

    :param trigger: [description]
    :type trigger: [type]
    """
    body = {}
    non_mutable_keys = [
        "accountId",
        "containerId",
        "fingerprint",
        "parentFolderId",
        "path",
        "tagManagerUrl",
        "triggerId",
        "workspaceId",
    ]

    for k, v in trigger.items():
        if k not in non_mutable_keys:
            body[k] = v
    return body
