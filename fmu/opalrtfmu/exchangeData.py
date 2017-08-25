# -----------------------------------------------------------------------------
# This example shows how to use the Python API to make a connection
# to a current running (or paused) model. It also shows how to
# change the current state of the model using the pause and
# execute command. In this simple example, the current model state
# is toggled between paused and executed
#
# WARNING: Before running this script, verify that the model is compiled and is
# running (or paused)
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
#  Import modules
# -----------------------------------------------------------------------------
## Import OpalApi module for Python
import RtlabApi
import os, sys


# -----------------------------------------------------------------------------
#  Script core
# -----------------------------------------------------------------------------
## if the script is executed (not imported)
def exchangeData(projectPath, inputNames, inputValues, outputNames, simulationTime):
    """
    Function to exchange data with a running model.
    
    :param projectPath: Path to the project file.
    :param inputNames: Input signal names of the  model.
    :param outputNames: Input signal values of the  model.
    :param outputNames: Output signal names of the  model.
    :param simulationTime: Model simulation time.
    
    """

    ## Connect to a running model using its name. The system
    ## control is release     
    projectName = os.path.abspath(projectPath)
    RtlabApi.OpenProject(projectName)
    
    print ("The connection with {!s} is completed.".format(projectName))

    try:
        ## Get the model state and the real simulationTime mode
        modelState, realTimeMode = RtlabApi.GetModelState()
                
        ## Print the model state
        print ("- The model state is {!s}.".format(RtlabApi.OP_MODEL_STATE(modelState)))
        
        ## If the model is running
        if modelState == RtlabApi.MODEL_RUNNING:
            ## Exchange data
            try:
                outputValues = RtlabApi.GetSignalsByName(outputNames)
            except Exception:
                ## Ignore error 11 which is raised when
                ## RtlabApi.DisplayInformation is called whereas there is no
                ## pending message
                info = sys.exc_info()
                if info[1][0] <> 11:  # 'There is currently no data waiting.'
                    ## If a exception occur: stop waiting
                    print ("An error occured at simulationTime={!s} while getting the " \
                           "output values for the output names={!s}.".format(simulationTime, outputNames))
                    raise
            try:
                #signalNames = (signalName1, signalName2, ...)
                #signalValues = (value1, value2, ...)
                #RtlabApi.SetSignalsByName(signalNames, signalValues)
                RtlabApi.SetSignalsByName(inputNames, inputValues)
            except Exception:
                ## Ignore error 11 which is raised when
                ## RtlabApi.DisplayInformation is called whereas there is no
                ## pending message
                info = sys.exc_info()
                if info[1][0] <> 11:  # 'There is currently no data waiting.'
                    ## If a exception occur: stop waiting
                    print ("An error occured at simulationTime={!s} while setting the " \
                           "input values for the input names={!s}.".format(simulationTime, inputNames))
                    raise
           
        ## if the model is not running
        else:
            ## Print the model state
            print ("- The model state is not running. Simulation will be terminated.")
            raise

    
    finally:
        ## Always disconnect from the model when the connection
        ## is completed
        stopTime = RtlabApi.GetStopTime()
        if (simulationTime < stopTime):
            RtlabApi.Disconnect()
            print ("The connection is closed.")
        else:
            # Check if I need to terminate the model
            # Needs to know what Reset() does and 
            # whether after calling reset the model needs 
            # to be recompiled and loaded again?
            RtlabApi.Reset()
            RtlabApi.Disconnect()
            print ("The simulation stop simulationTime={!s} is reached. "\
                   "The model is reset and the connection is closed.".format(stopTime))
