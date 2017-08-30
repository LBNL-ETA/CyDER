# -----------------------------------------------------------------------------
# This script contains functions which are used
# to communicate with Opal RT through the RT-Lab
# Python API. The Python API is used to compile
# a model, load the model, and execute a model.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
#  Import modules
# -----------------------------------------------------------------------------
## Import OpalApi module for Python
import RtlabApi
from time import sleep
import os
import sys
from datetime import datetime

def compileAndInstantiate(projectPath):
    """
    Function to compile, load, and execute a model.

    :param projectPath: Path to the project file.

    """

    # Check if MetaController is running and if not start it up

    import subprocess
    # Start the MetaController
    tasklist = subprocess.check_output('tasklist', shell=True)
    if not "MetaController.exe" in tasklist:
        print("=====Starting the MetaController.")
        try:
            subprocess.Popen("MetaController")
        except:
            print("=====MetaController.exe couldn't be started. ")
            print("=====Check that the \\common\\bin folder of RT-Lab is on the system PATH.")
            raise

        print("=====MetaController is successfully started.")

    # Wait 1 second to give time to the MetaController to start
    sleep(1.0)
    projectName = os.path.abspath(projectPath)
    print("=====Path to the project={!s}".format(projectName))

    ## Open a model using its name.
    RtlabApi.OpenProject(projectName)
    print ("=====The connection with {!s} is completed.".format(projectName))

    # Check if model was already compiled and is already running
    try:
        ## Get the model state and the real time mode
        modelState, realTimeMode = RtlabApi.GetModelState()

        ## Print the model state
        print ("=====The model state is {!s}.".format(RtlabApi.OP_MODEL_STATE(modelState)))

        ## If the model is running
        if modelState == RtlabApi.MODEL_RUNNING:
            #print("This is the output value={!s}".format(RtlabApi.GetSignalsByName('sm_computation.reference_out')))
            ## Pause the model
            print ("=====The model is running and won't be recompiled.")
            RtlabApi.Disconnect()
            return

    except Exception:
        ## Ignore error 11 which is raised when
        ## RtlabApi.DisplayInformation is called whereas there is no
        ## pending message
        info = sys.exc_info()
        if info[1][0] != 11:  # 'There is currently no data waiting.'
            ## If a exception occur: stop waiting
            print ("An error occured during compilation.")
            #raise

    start = datetime.now()

    mdlFolder, mdlName = RtlabApi.GetCurrentModel()
    mdlPath = os.path.join(mdlFolder, mdlName)

    try:
        ## Registering this thread to receive all messages from the controller
        ## (used to display compilation log into python console)
        RtlabApi.RegisterDisplay(RtlabApi.DISPLAY_REGISTER_ALL)

        ## Set attribute on project to force to recompile (optional)
        modelId = RtlabApi.FindObjectId(RtlabApi.OP_TYPE_MODEL, mdlPath)
        RtlabApi.SetAttribute(modelId, RtlabApi.ATT_FORCE_RECOMPILE, True)

        ## Launch compilation
        compilationSteps = RtlabApi.OP_COMPIL_ALL_NT | RtlabApi.OP_COMPIL_ALL_LINUX
        RtlabApi.StartCompile2((("", compilationSteps), ), )
        print ("=====Compilation started.")

        ## Wait until the end of the compilation
        status = RtlabApi.MODEL_COMPILING
        while status == RtlabApi.MODEL_COMPILING:
            try:
                ## Check status every 0.5 second
                sleep(0.5)

                ## Get new status
                ## To be done before DisplayInformation because
                ## DisplayInformation may generate an Exception when there is
                ## nothing to read
                status, _ = RtlabApi.GetModelState()

                ## Display compilation log into Python console
                _, _, msg = RtlabApi.DisplayInformation(1)
                while len(msg) > 0:
                    print (msg),
                    _, _, msg = RtlabApi.DisplayInformation(1)

            except Exception:
                ## Ignore error 11 which is raised when
                ## RtlabApi.DisplayInformation is called whereas there is no
                ## pending message
                info = sys.exc_info()
                if info[1][0] != 11:  # 'There is currently no data waiting.'
                    ## If a exception occur: stop waiting
                    print ("An error occured during compilation.")
                    raise

        ## Because we use a comma after print when forward compilation log into
        ## Python log we have to ensure to write a carriage return when
        ## finished.
        print('')

        ## Get project status to check is compilation succeed
        status, _ = RtlabApi.GetModelState()
        if status == RtlabApi.MODEL_LOADABLE:
            print ("=====Compilation success.")
        else:
            print ("=====Compilation failed.")

        ## Load the current model
        realTimeMode = RtlabApi.HARD_SYNC_MODE  # Also possible to use SIM_MODE, SOFT_SIM_MODE, SIM_W_NO_DATA_LOSS_MODE or SIM_W_LOW_PRIO_MODE
        timeFactor   = 1
        RtlabApi.Load(realTimeMode, timeFactor)
        print ("=====The model is loaded.")

        try:
            ## Execute the model
            RtlabApi.Execute(1)
            print ("=====The model executes for the first time.")

        except Exception:
            ## Ignore error 11 which is raised when
            ## RtlabApi.DisplayInformation is called whereas there is no
            ## pending message
            info = sys.exc_info()
            if info[1][0] != 11:  # 'There is currently no data waiting.'
                ## If a exception occur: stop waiting
                print ("An error occured during execution.")
                raise

        end = datetime.now()
        print(
            'Compiled, loaded and executed the model for the first time in {!s} seconds.'.format(
                (end - start).total_seconds()))
    finally:
        ## Always disconnect from the model when the connection is completed
        print ("The model has been successfully compiled and is now running.")
        RtlabApi.Disconnect()

def setData(projectPath, inputNames, inputValues, simulationTime):
    """
    Function to exchange data with a running model.

    :param projectPath: Path to the project file.
    :param inputNames: Input signal names of the  model.
    :param inputValues: Input signal values of the  model.
    :param simulationTime: Model simulation time.

    """

    sleep(1.0)
    projectName = os.path.abspath(projectPath)
    print("=====Path to the project={!s}".format(projectName))

    start = datetime.now()
    RtlabApi.OpenProject(projectName)
    print ("=====The connection with {!s} is completed.".format(projectName))
    try:
        ## Get the model state and the real simulationTime mode
        modelState, realTimeMode = RtlabApi.GetModelState()

        ## Print the model state
        print ("=====The model state is {!s}.".format(RtlabApi.OP_MODEL_STATE(modelState)))

        ## If the model is running
        if modelState == RtlabApi.MODEL_RUNNING:
            ## Set input data
            ########Setting inputs of the model
            try:
                #signalNames = (signalName1, signalName2, ...)
                #signalValues = (value1, value2, ...)
                #RtlabApi.SetSignalsByName(signalNames, signalValues)
                ## Get signal control before changing values
                signalControl = 1
                RtlabApi.GetSignalControl(signalControl)
                print ("=====The signal control is acquired.")
                RtlabApi.SetSignalsByName(inputNames, inputValues)
                ## Release signal control after changing values
                signalControl = 0
                RtlabApi.GetSignalControl(signalControl)
                print ("=====The signal control is released.")
            except Exception:
                ## Ignore error 11 which is raised when
                ## RtlabApi.DisplayInformation is called whereas there is no
                ## pending message
                info = sys.exc_info()
                if info[1][0] != 11:  # 'There is currently no data waiting.'
                    ## If a exception occur: stop waiting
                    print ("An error occured at simulationTime={!s} while setting the " \
                           "input values for the input names={!s}.".format(simulationTime, inputNames))
                    raise
        ## if the model is not running
        else:
            ## Print the model state
            print ("The model state is not running. Simulation will be terminated.")
            raise
        end = datetime.now()
        print(
            'Send values={!s} of inputs with names={!s} in {!s} seconds.'.format(inputValues,
            inputNames, (end - start).total_seconds()))
    finally:
        ## Always disconnect from the model when the connection
        ## is completed
        stopTime = RtlabApi.GetStopTime()
        print ("=====The simulation stoptime={!s}.".format(stopTime))
        if (simulationTime <= stopTime):
            RtlabApi.Disconnect()
            print ("=====The connection is closed.")
        else:
            # Check if I need to terminate the model
            # Needs to know what Reset() does and
            # whether after calling reset the model needs
            # to be recompiled and loaded again?
            RtlabApi.Reset()
            RtlabApi.Disconnect()
            print ("=====The simulation stoptime={!s} is reached. "\
                   "The model is reset and the connection is closed.".format(stopTime))


def getData(projectPath, outputNames, simulationTime):
    """
    Function to exchange data with a running model.

    :param projectPath: Path to the project file.
    :param outputNames: Output signal names of the  model.
    :param simulationTime: Model simulation time.

    """

    ## Connect to a running model using its name.
    sleep(1.0)
    projectName = os.path.abspath(projectPath)
    print("=====Path to the project={!s}".format(projectName))

    start = datetime.now()
    RtlabApi.OpenProject(projectName)
    print ("=====The connection with {!s} is completed.".format(projectName))
    try:
        ## Get the model state and the real simulationTime mode
        modelState, realTimeMode = RtlabApi.GetModelState()

        ## Print the model state
        print ("=====The model state is {!s}.".format(RtlabApi.OP_MODEL_STATE(modelState)))

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
                if info[1][0] != 11:  # 'There is currently no data waiting.'
                    ## If a exception occur: stop waiting
                    print ("An error occured at simulationTime={!s} while getting the " \
                           "output values for the output names={!s}.".format(simulationTime, outputNames))
                    raise

        ## if the model is not running
        else:
            ## Print the model state
            print ("The model state is not running. Simulation will be terminated.")
            raise

        end = datetime.now()
        print(
            'Get values={!s} of outputs with names={!s} in {!s} seconds.'.format(outputValues,
            outputNames, (end - start).total_seconds()))
    finally:
        ## Always disconnect from the model when the connection
        ## is completed
        stopTime = RtlabApi.GetStopTime()
        print ("=====The simulation stoptime={!s}.".format(stopTime))
        if (simulationTime <= stopTime):
            RtlabApi.Disconnect()
            print ("=====The connection is closed.")
        else:
            # Check if I need to terminate the model
            # Needs to know what Reset() does and
            # whether after calling reset the model needs
            # to be recompiled and loaded again?
            RtlabApi.Reset()
            RtlabApi.Disconnect()
            print ("=====The simulation stoptime={!s} is reached. "\
                   "The model is reset and the connection is closed.".format(stopTime))

    return outputValues

def convertUnicodeString(inputNames):
    """
    This function gets an unicode string and convert it to a string.
    """
    retNames = []
    if (isinstance(inputNames, list)):
        for elem in inputNames:
            retNames.append(str(elem))
    else:
        retNames = str(inputNames)

    return retNames


def exchange(projectPath, simulationTime, inputNames, inputValues, outputNames, writeResults):

#if __name__ == "__main__":

    ## Connect to a running model using its name.
    #projectName = os.path.abspath(os.path.join('examples', 'demo', 'demo.llp'))

     """
     This function is used to exchange data with the Opal RT FMU.

     """

     # This is just for testing and will be retrieved from the project path
     projectName = "D:\\Users\\emma\\Documents\\GitHub\\CyDER\\cosimulation\\source\\generate_fmu\\fmu\\opalrtfmu\\examples\\demo\\demo.llp"

     # Convert the input and output names to be strings that can be set in Opal-RT models
     #inputNames = 'demo/sc_user_interface/port1'
     #inputNames = None
     #inputValues = 1.0
     #outputNames = ['demo/sm_computation/port1', 'demo/sm_computation/port2', 'demo/sm_computation/port3']
     if (inputNames is not None):
         inputNames=convertUnicodeString(inputNames)
     if (outputNames is not None):
        outputNames=convertUnicodeString(outputNames)

     print ("=====Ready to compile, load, and execute the model.")
     # Compile and Run the model for the first time
     compileAndInstantiate(projectName)


     simulationTime = 0.0
     print ("=====Ready to exchange data with the OPAL-RT running model.")
     # Handle the case when inputNames is None

     if(inputNames is not None):
         print ("=====Ready to set the input variables={!s} with values={!s} at time={!s}.".format(inputNames, inputValues, simulationTime))
         if (isinstance(inputNames, list)):
             len_inputNames = len(inputNames)
             len_inputValues = len(inputValues)
             if(len_inputNames<>len_inputValues):
                 print ("An error occured at simulationTime={!s}. "\
                         "Length of inputNames={!s} ({!s}) does not match " \
                         "length of input values={!s} ({!s}).".format(simulationTime, inputNames,
                         len_inputNames, inputValues, len_inputValues))
                 raise
             setData(projectName, tuple(inputNames), tuple(inputValues), simulationTime)
         else:
             setData(projectName, inputNames, inputValues, simulationTime)
         print("=====The input variables={!s} were successfully set.".format(inputNames))

     if (outputNames is not None):
         print ("=====Ready to get the output variables={!s} at time={!s}.".format(outputNames, simulationTime))
         if (isinstance(outputNames, list)):
             outputValues = getData(projectName, tuple(outputNames), simulationTime)
             len_outputNames = len(outputNames)
             len_outputValues = len(outputValues)
             if(len_outputNames<>len_outputValues):
                 print ("An error occured at simulationTime={!s}. "\
                         "Length of outputNames={!s} ({!s}) does not match " \
                         "length of output values={!s} ({!s}).".format(simulationTime, outputNames,
                         len_outputNames, outputValues, len_outputValues))
                 raise
             outputValues = getData(projectName, tuple(outputNames), simulationTime)
         else:
             outputValues = getData(projectName, outputNames, simulationTime)
         print("=====The output variables={!s} were successfully retrieved.".format(outputNames))
         if(outputValues is None):
             print ("output values for outputNames={!=} is empty at time={!s}.".
                    format(outputNames, simulationTime))
             raise
         print ("=====The values of the output variables:{!s} are equal {!s} at time={!s}.".format(outputNames,
                 outputValues, simulationTime))

     # Convert the output values to float so they can be used on the receiver side.
     retOutputValues = []
     print("The outputValues are={!s}".format(outputValues))
     if (isinstance(outputValues, tuple)):
         for elem in outputValues:
             retOutputValues.append(1.0*float(elem))
     else:
         retOutputValues = 1.0 * float (outputValues)

     return retOutputValues

#if __name__ == "__main__":

    ## Connect to a running model using its name.
    #projectName = os.path.abspath(os.path.join('examples', 'demo', 'demo.llp'))
