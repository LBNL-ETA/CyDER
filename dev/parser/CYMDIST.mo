model CYMDIST
  "Block that exchanges a vector of real values with CYMDIST"
  extends Modelica.Blocks.Interfaces.DiscreteBlock(
    startTime=0,
    firstTrigger(fixed=true, start=false));
  parameter Real par1(unit="Ohm") = 1.0
    "First parameter";
  parameter Real par2(unit="Ohm") = 10.0
    "Second parameter";
  Modelica.Blocks.Interfaces.RealInput u(start=1.0, unit="A")
    "First input";
  Modelica.Blocks.Interfaces.RealOutput y (unit="V")
    "First output";
  Modelica.Blocks.Interfaces.RealInput u1(start=2.0, unit="A")
    "Second input";
  Modelica.Blocks.Interfaces.RealOutput y1 (unit="V")
    "Second output";
 
protected   
  parameter String moduleName
    "Name of the python module that contains the function";
  parameter String functionName=moduleName "Name of the python function";
  parameter Integer nDblPar = 2 
    "Number of double parameter values to sent to CYMDIST";
  parameter Integer nDblInp(min=1) = 2 
    "Number of double input values to sent to CYMDIST";
  parameter Integer nDblOut(min=1) = 2  
    "Number of double output values to receive from CYMDIST";
  parameter Integer flaDblInp[nDblInp] = zeros(nDblInp)
    "Flag for double values (0: use current value, 
    1: use average over interval, 2: use integral over interval)";
  
  Real uR[nDblInp]={
  u,
  u1 
  }"Variables used to collect values to be sent to CYMDIST";
  
  Real yR[nDblOut]={
  y,
  y1 

  }"Variable used to collect values received from CYMDIST";
  Real uRInt[nDblInp] "Value of integral";
  Real uRIntPre[nDblInp] "Value of integral at previous sampling instance";
  Real dblInpVal[nDblInp] "Value to be sent to CYMDIST";
  
  parameter String dblInpNam[nDblInp] = {
  "u",
  "u1" 
  }"Input variables names to be sent to CYMDIST";
  
  parameter String dblOutNam[nDblOut] = {
  "y",
  "y1" 
  }"Output variables names to be received from CYMDIST";
  
  parameter String dblParNam[nDblPar] = {
  "par1",
  "par2"
  }"Parameter variables names to be sent to CYMDIST";

  parameter Real dblParVal[nDblPar] = {
  1.0,
  10.0
  }"Parameter variables values to be sent to CYMDIST";

  
initial equation 
  dblInpVal    =  pre(uR);
  uRInt    =  zeros(nDblInp);
  uRIntPre =  zeros(nDblInp);
  for i in 1:nDblInp loop
    assert(flaDblInp[i]>=0 and flaDblInp[i]<=2,
      "Parameter flaDblInp out of range for " + String(i) + "-th component.");
  end for;
  // The assignment of yR avoids the warning
  // "initial conditions for variables of type Real are not fully specified".
  // At startTime, the sampleTrigger is true and hence this value will
  // be overwritten.

  yR = zeros(nDblOut);
equation 
  for i in 1:nDblInp loop
    der(uRInt[i]) = if (flaDblInp[i] > 0) then uR[i] else 0;
  end for;
   
  when {sampleTrigger} then
    // Compute value that will be sent to CYMDIST
    for i in 1:nDblInp loop
      if (flaDblInp[i] == 0) then
        // Send the current value.
        dblInpVal[i] = pre(uR[i]); 
      else
        // Integral over the sampling interval
        dblInpVal[i] = uRInt[i] - pre(uRIntPre[i]);
        if (flaDblInp[i] == 1) then
          // Average value over the sampling interval
          dblInpVal[i] =  dblInpVal[i]/samplePeriod;  
        end if;
      end if;
    end for;
      
    // Exchange data
    yR = Buildings.Utilities.IO.Python27.Functions.cymdist(
      moduleName=moduleName,
      functionName=functionName,
      nDblInp=nDblInp,
      dblInpNam=dblInpNam,
      dblInpVal=dblInpVal,
      nDblOut=nDblOut,
      dblOutNam=dblOutNam,
      nDblPar=nDblPar,
      dblParNam=dblParNam,
      dblParVal=dblParVal);
  // Store current value of integral
  uRIntPre= uRInt;
  end when;    
end CYMDIST;