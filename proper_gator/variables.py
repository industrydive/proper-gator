from proper_gator.service import execute


def get_variables(service, workspace):
    variables = execute(
        service.accounts()
        .containers()
        .workspaces()
        .variables()
        .list(parent=workspace["path"])
    )

    return variables


def clone_variables(service, target_workspace, destination_workspace):
    """For each variable in the target_workspace, create a variable in each of the
    destination workspaces. If

    :param service: [description]
    :type service: [type]
    :param target_workspace: [description]
    :type target_workspace: [type]
    :param destination_workspaces: [description]
    :type destination_workspaces: [type]
    """
    variable_mapping = {}
    variables_wrapper = get_variables(service, target_workspace)
    for variable in variables_wrapper["variable"]:
        variable_body = create_variable_body(variable)
        new_variable = create_variable(service, destination_workspace, variable_body)
        variable_mapping[variable["variableId"]] = new_variable["variableId"]
    return variable_mapping


def create_variable_body(variable):
    """Given a variable, remove all keys that are specific to that variable
    and return keys + values that can be used to clone another variable

    https://googleapis.github.io/google-api-python-client/docs/dyn/variablemanager_v2.accounts.containers.workspaces.variables.html#create

    :param variable: [description]
    :type variable: [type]
    """
    body = {}
    non_mutable_keys = [
        "accountId",
        "containerId",
        "fingerprint",
        "parentFolderId",
        "path",
        "tagManagerUrl",
        "variableId",
        "workspaceId",
    ]

    for k, v in variable.items():
        if k not in non_mutable_keys:
            body[k] = v
    return body


def create_variable(service, workspace, variable_body):
    new_variable = execute(
        service.accounts()
        .containers()
        .workspaces()
        .variables()
        .create(parent=workspace["path"], body=variable_body)
    )
    return new_variable
