from __future__ import division
import models as m
import tool as t
import pdb


def simulate(pk):
    """
    Launch a simulation from a model_user id
    """
    # Get the model id from the model user id
    try:
        user_model = m.UserModel.objects.get(id=pk)
    except:
        raise Exception("Model User " + str(pk) + " does not exist")

    # Get the model corresponding to it
    model = user_model.model

    # Launch simulation
    timeout = False
    arg = [str(model.filename)]
    cmd = ('project_cyder/web/docker_django/worker/simulation.py')
    output, status = t.run_ssh_command(cmd, timeout=timeout, arg=arg)

    # Parse the results
    result = t.parse_ssh_list(output, status)

    # Wipe out previous results if any
    m.NodeResult.objects.filter(usermodel=user_model).delete()

    # Save results back to the database
    [m.NodeResult(usermodel=user_model, **node).save() for node in results]

    return result
