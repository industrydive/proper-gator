from proper_gator.service import execute


def get_variables(service, workspace):
    """Get all variables that exist in a given workspace

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param workspace: A Google Tag Manager workspace
    :type workspace: dict
    :return: A collection of variables in the Google Tag Manager List Response format
    :rtype: dict
    """
    variables = execute(
        service.accounts()
        .containers()
        .workspaces()
        .variables()
        .list(parent=workspace["path"])
    )

    return variables


def create_variable(service, workspace, variable_body):
    """Create a variable in a given workspace

    https://googleapis.github.io/google-api-python-client/docs/dyn/tagmanager_v2.accounts.containers.workspaces.variables.html#create

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param workspace: A Google Tag Manager workspace
    :type workspace: dict
    :param variable_body: The request body that the variable should be created with
    :type variable_body: dict
    :return: The created variable
    :rtype: dict
    """
    new_variable = execute(
        service.accounts()
        .containers()
        .workspaces()
        .variables()
        .create(parent=workspace["path"], body=variable_body)
    )
    print(
        f"Created {variable_body['name']} in "
        f"{workspace['name']} - {workspace['conta inerId']}"
    )
    return new_variable


def clone_variables(service, target_workspace, destination_workspace):
    """For each variable in the target_workspace, create a variable in each of the
    destination workspaces.

    :param service: The Google service object
    :type service: googleapiclient.discovery.Resource
    :param target_workspace: The Google Tag Manager workspace to clone variables from
    :type target_workspace: dict
    :param destination_workspace: A Google Tag Manager workspace to clone variables to
    :type destination_workspace: dict
    :return: A mapping of the variable ids from the target workspace to the variable ids
             in the destination workspace.
    :rtype: dict
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

    :param variable: The variable to convert into a request body
    :type variable: dict
    :return: A request body to be used in the create variable method
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
        "variableId",
        "workspaceId",
    ]

    for k, v in variable.items():
        if k not in non_mutable_keys:
            body[k] = v
    return body
