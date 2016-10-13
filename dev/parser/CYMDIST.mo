model CYMDIST
    "Block that exchanges a vector of real values with a Python function"
    extends Modelica.Blocks.Interfaces.DiscreteBlock(
      startTime=0,
      firstTrigger(fixed=true, start=false));
    parameter Real par1(unit="Ohm")
      "First parameter";
    parameter Real par2(unit="Ohm")
      "Second parameter";
    Modelica.Blocks.Interfaces.RealInput u(start="1.0", unit="A")
      "First input";
    Modelica.Blocks.Interfaces.RealOutput y (unit="V")
      "First output";
    Modelica.Blocks.Interfaces.RealInput u1(start="2.0", unit="A")
      "Second input";
    Modelica.Blocks.Interfaces.RealOutput y1 (unit="V")
      "Second output";
    
    parameter Integer nDblWri(min=1) = 2 
      "Number of double values to sent to CYMDIST";
    parameter Integer nDblRea(min=1) = 2  
      "Number of double values to read from CYMDIST";
    parameter Integer flaDblWri[nDblWri] = zeros(nDblWri)
    "Flag for double values (0: use current value, 1: use average over interval, 2: use integral over interval)";
    
    Real uR[nDblWri] "Real inputs to be sent to CYMDIST";
    Real yR[nDblRea] "Real outputs received from CYMDIST";

    Real uRInt[nDblWri] "Value of integral";
    Real uRIntPre[nDblWri] "Value of integral at previous sampling instance";
    Real uRWri[nDblWri] "Value to be sent to CYMDIST";
    
    parameter String uRStr[nDblWri] = ["u", "u1"] 
      "Input variables names to be sent to CYMDIST";
    
    parameter String yRStr[nDblWri] = ["y", "y1"] 
      "Output variables names to be read from CYMDIST";

initial equation 
    
    uR[1] = u;
    uR[2] = u1; 
    uRWri    =  pre(uR);
    uRInt    =  zeros(nDblWri);
    uRIntPre =  zeros(nDblWri);
    for i in 1:nDblWri loop
      assert(flaDblWri[i]>=0 and flaDblWri[i]<=2,
        "Parameter flaDblWri out of range for " + String(i) + "-th component.");
    end for;
    // The assignment of yR avoids the warning
    // "initial conditions for variables of type Real are not fully specified".
    // At startTime, the sampleTrigger is true and hence this value will
    // be overwritten.
    yR = zeros(nDblRea);
equation 
    uR[1] = u;
    uR[2] = u1;
    yR[1] = y;
    yR[2] = y1;
    for i in 1:nDblWri loop
      der(uRInt[i]) = if (flaDblWri[i] > 0) then uR[i] else 0;
    end for;
   
    when {sampleTrigger} then
      // Compute value that will be sent to CYMDIST
      for i in 1:nDblWri loop
        if (flaDblWri[i] == 0) then
          // Send the current value.
          uRWri[i] = pre(uR[i]); 
        else
          // Integral over the sampling interval
          uRWri[i] = uRInt[i] - pre(uRIntPre[i]);
          if (flaDblWri[i] == 1) then
            // Average value over the sampling interval
            uRWri[i] =  uRWri[i]/samplePeriod;  
          end if;
        end if;
      end for;
      
      // Exchange data
      yR = Buildings.Utilities.IO.Python27.Functions.cymdist(
        moduleName=moduleName,
        functionName=functionName,
        dblWri=uRWri,
        nDblWri=nDblWri,
        nDblRea=nDblRea,
        dlbWriNam=uRStr,
        dlbReaNam=yRStr);
      
    // Store current value of integral
    uRIntPre= uRInt;
    end when;    
end CYMDIST;