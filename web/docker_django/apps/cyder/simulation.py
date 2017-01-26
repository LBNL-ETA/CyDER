from __future__ import division
import models as m


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
    pass
