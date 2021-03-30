from proper_gator.service import execute


def get_triggers(service, workspace):
    triggers = execute(
        service.accounts()
        .containers()
        .workspaces()
        .triggers()
        .list(parent=workspace["path"])
    )

    return triggers


def create_trigger(service, workspace, trigger_body):
    new_trigger = execute(
        service.accounts()
        .containers()
        .workspaces()
        .triggers()
        .create(parent=workspace["path"], body=trigger_body)
    )
    return new_trigger


def clone_triggers(service, target_workspace, destination_workspace):
    """For each trigger in the target_workspace, create a trigger in each of the
    destination workspaces. If

    :param service: [description]
    :type service: [type]
    :param target_workspace: [description]
    :type target_workspace: [type]
    :param destination_workspaces: [description]
    :type destination_workspaces: [type]
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
