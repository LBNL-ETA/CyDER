This folder contains two FMUs which are used
to test if PyFMi can handle algebraic loop.

The first FMU (FirstModel.fmu) implements y = u (u is the input, y is the output)
The second FMU (SecondModel.fmu) implements y = u*u (u is the input, y is the output)

These two FMUs are linked to form a coupled system by
connecting the output of the first model
with the input of the second modle, and the output of the 
second model to the input of the first model
This forms an algebraic loop which leads to the equation u = u*u
        