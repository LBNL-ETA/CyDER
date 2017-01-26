from __future__ import division
import models as m
import tool as t


def simulate(pk):
    """
    Launch a simulation from a model_user id
    """
    # Get the model id from the model user id
    try:
        model_user = m.UserModel.objects.get(id=pk)
    except:
        raise Exception("Model User " + str(pk) + " does not exist")

    # Get the model corresponding to it
    model = model_user.model

    # Launch simulation
    timeout = 30
    arg = [str(model.filename)]
    cmd = ('project_cyder/web/docker_django/worker/simulation.py')
    output, status = t.run_ssh_command(cmd, timeout=timeout, arg=arg)

    # Parse the results
    result = t.parse_ssh_list(output, status)

    return result
