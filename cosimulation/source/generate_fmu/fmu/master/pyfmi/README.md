# Co-simulation 


## Overview

PyFMI version 2.3.1 and higher can be used to link GridDyn with CYMDIST. 
We note that PyFMI version 2.3.1 only supports FMUs 2.0 for co-simulation.
Therefore all FMUs developed within this project should be FMUs for co-simulation
2.0. This has the drawback that we use a speficiaction which is flawed as it does not allow
to simulate direct feedthrough models as those types of models require the ability to call 
fmi2DoStep() with a zero step length.