from __future__ import division
import models as m
import tool as t
import pdb


def simulate(pk, nb_vehicles=False):
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
    if not nb_vehicles:
        timeout = False
        arg = [str(model.filename)]
        cmd = ('project_cyder/web/docker_django/worker/simulation.py')
        output, status = t.run_ssh_command(cmd, timeout=timeout, arg=arg)
    else:
        timeout = False
        arg = [str(model.filename), str(int(nb_vehicles))]
        cmd = ('project_cyder/web/docker_django/worker/simulation_vehicle.py')
        output, status = t.run_ssh_command(cmd, timeout=timeout, arg=arg)

    # Parse the results
    result = t.parse_ssh_list(output, status)

    # Wipe out previous results if any
    m.NodeResult.objects.filter(usermodel=user_model).delete()

    # Change "None" to None
    for index, node in enumerate(result):
        for key, value in node.items():
            if value == "None":
                result[index][key] = None

    # Save results back to the database
    [m.NodeResult(usermodel=user_model, **node).save() for node in result]

    return result
