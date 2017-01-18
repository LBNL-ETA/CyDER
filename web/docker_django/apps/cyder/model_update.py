from __future__ import division
import models as m
import tool as t


def update_model_devices(model_id):
    """
    Update the nodes for a model, return the number of nodes.
    """
    # Query the model information
    try:
        model_instance = m.Model.objects.get(id=model_id)
    except:
        raise Exception('Model id does not exist in the database')

    # Get the node data
    devices = get_model_content_data('model_devices.py', model_instance.filename)

    # Update the database
    for device in devices:
        temp = m.Devices(model=model_instance, **device)
        temp.save()

    return len(devices)


def update_model_nodes(model_id):
    """
    Update the nodes for a model, return the number of nodes.
    """
    # Query the model information
    try:
        model_instance = m.Model.objects.get(id=model_id)
    except:
        raise Exception('Model id does not exist in the database')

    # Get the node data
    nodes = get_model_content_data('model_nodes.py', model_instance.filename)

    # Update the database
    for node in nodes:
        temp = m.Node(model=model_instance, **node)
        temp.save()

    return len(nodes)


def get_model_content_data(script, filename):
    """
    Launch ssh command and retrieve outputs
    """
    # Launch SSH request to the server and grab the stdout
    timeout = False
    cmd = 'project_cyder/web/docker_django/worker/' + script + ' ' + str(filename)
    output, status = t.run_ssh_command(cmd, timeout=timeout)

    # Parse ssh output
    if output is not False:
        result = t.parse_dataframe_ssh_output(output, status)
    else:
        raise Exception('SSH request to the server took more than ' +
                        str(timeout) + ' seconds')

    # Return the value from the calibration
    return result
