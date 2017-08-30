# -----------------------------------------------------------------------------
# This script shows how to use the Python API to compile a model,
# load the model, and execute the model. Subsequent calls to this 
# script will not recompile the model if it is already running.
# -----------------------------------------------------------------------------


# -----------------------------------------------------------------------------
#  Import modules
# -----------------------------------------------------------------------------
## Import OpalApi module for Python
import RtlabApi
from time import sleep
import os
import sys

# -----------------------------------------------------------------------------
#  Script core
# -----------------------------------------------------------------------------
def compileAndInstantiate(projectPath):
    """
    Function to compile, load, and execute a model.
    
    :param projectPath: Path to the project file.
    
    """

    ## Connect to a running model using its name. The system
    ## control is release     
    projectName = os.path.abspath(projectPath)
    RtlabApi.OpenProject(projectName)
        
    print ("The connection with {!s} is completed.".format(projectName))
    
    # Check if model was already compiled and is already running
    try:
        ## Get the model state and the real time mode
        modelState, realTimeMode = RtlabApi.GetModelState()
                
        ## Print the model state
        print ("- The model state is {!s}.".format(RtlabApi.OP_MODEL_STATE(modelState)))
    
        ## If the model is running
        if modelState == RtlabApi.MODEL_RUNNING:
            ## Pause the model
            return
           
    except Exception:
        ## Ignore error 11 which is raised when
        ## RtlabApi.DisplayInformation is called whereas there is no
        ## pending message
        info = sys.exc_info()
        if info[1][0] <> 11:  # 'There is currently no data waiting.'
            ## If a exception occur: stop waiting
            print ("An error occured during compilation.")
            raise
        
    
    ## Get path to model
    models = RtlabApi.GetActiveModels()
    mdlFileName, mdlFolder, _, _, _, _, _ = models[0]
    mdlPath = os.path.join(mdlFolder, mdlFileName)
    
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
        print ("Compilation started.")

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
                    print msg,
                    _, _, msg = RtlabApi.DisplayInformation(1)
                
            except Exception:
                ## Ignore error 11 which is raised when
                ## RtlabApi.DisplayInformation is called whereas there is no
                ## pending message
                info = sys.exc_info()
                if info[1][0] <> 11:  # 'There is currently no data waiting.'
                    ## If a exception occur: stop waiting
                    print ("An error occured during compilation.")
                    raise
        
        ## Because we use a comma after print when forward compilation log into
        ## Python log we have to ensure to write a carriage return when
        ## finished.
        print ''
        
        ## Get project status to check is compilation succeed
        status, _ = RtlabApi.GetModelState()
        if status == RtlabApi.MODEL_LOADABLE:
            print ("Compilation success.")
        else:
            print ("Compilation failed.")
            
        ## Load the current model
        realTimeMode = RtlabApi.HARD_SYNC_MODE  # Also possible to use SIM_MODE, SOFT_SIM_MODE, SIM_W_NO_DATA_LOSS_MODE or SIM_W_LOW_PRIO_MODE
        timeFactor   = 1
        RtlabApi.Load(realTimeMode, timeFactor)
        print ("- The model is loaded.")

        try:
            ## Execute the model
            RtlabApi.Execute(1)
            
            print ("- The model executes for the first time.")

        except Exception, exc:
            ## Ignore error 11 which is raised when
            ## RtlabApi.DisplayInformation is called whereas there is no
            ## pending message
            info = sys.exc_info()
            if info[1][0] <> 11:  # 'There is currently no data waiting.'
                ## If a exception occur: stop waiting
                print ("An error occured during execution.")
                raise
        

    finally:
        ## Always disconnect from the model when the connection is completed
        RtlabApi.Disconnect()
