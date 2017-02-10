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
        project = m.Project.objects.get(id=pk)
    except:
        raise Exception("Project " + str(pk) + " does not exist")
    project_models = m.ProjectModels.filter(project_id=project.id)


    if project_models:
        project_model = project_models[0]
    else:
        raise Exception("Project does not have any model")

    # Get the model corresponding to it
    model = project_model.model

    # Select the type of simulation
    vehicle_simulation = False
    try:
        scenario = m.ElectricVehicleScenario.objects.get(project_model=project_model)
        if scenario.is_active:
            vehicle_simulation = True
            nb_vehicles = scenario.nb_vehicles
    except:
        # No scenario in the database
        pass

    # Launch simulation
    if vehicle_simulation:
        timeout = False
        arg = [str(model.filename), str(int(nb_vehicles))]
        cmd = ('project_cyder/web/docker_django/worker/simulation_vehicle.py')
        output, status = t.run_ssh_command(cmd, timeout=timeout, arg=arg)
    else:
        timeout = False
        arg = [str(model.filename)]
        cmd = ('project_cyder/web/docker_django/worker/simulation.py')
        output, status = t.run_ssh_command(cmd, timeout=timeout, arg=arg)

    # Parse the results
    result = t.parse_ssh_list(output, status)

    # Wipe out previous results if any
    m.NodeResult.objects.filter(project_model=project_model).delete()

    # Change "None" to None
    for index, node in enumerate(result):
        for key, value in node.items():
            if value == "None":
                result[index][key] = None

    # Save results back to the database
    [m.NodeResult(project_model=project_model, **node).save() for node in result]

    return result
