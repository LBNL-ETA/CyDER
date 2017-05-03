within CYMDISTToFMU.Python34.Functions.BaseClasses;
function cymdist "Function that communicates with the CYMDISTToFMU Python API"
  input String moduleName
    "Name of the python module that contains the function";
  input String functionName=moduleName "Name of the python function";
  input String  conFilNam "Name of the python function";
  input Real    modTim[1] "Model time";
  input Real    dblParVal[nDblPar] "Parameter variables values to send to CYMDISTToFMU";
  input Real    dblInpVal[max(1, nDblInp)] "Input variables values to be sent to CYMDISTToFMU";
  input String  dblParNam[nDblPar] "Parameter variables names to send to CYMDISTToFMU";
  input String  dblOutNam[max(1, nDblOut)] "Output variables names to be read from CYMDISTToFMU";
  input String  dblInpNam[max(1, nDblInp)] "Input variables names to be sent to CYMDISTToFMU";
  input Integer nDblInp(min=0) "Number of double inputs to send to CYMDISTToFMU";
  input Integer nDblOut(min=0) "Number of double outputs to read from CYMDISTToFMU";
  input Integer nDblPar(min=0) "Number of double parameters to send to CYMDISTToFMU";
  input Real    resWri[1]  "Flag for enabling results writing. 1: write results, 0: else";
//   input Integer strLenRea(min=0)
//     "Maximum length of each string that is read. If exceeded, the simulation stops with an error";
  output Real    dblOutVal[max(1, nDblOut)] "Double output values read from CYMDISTToFMU";
  external "C" modelicaToCYMDIST(moduleName,
                                    functionName,
                                    conFilNam,
                                    modTim,
                                    nDblInp,
                                    dblInpNam,
                                    dblInpVal,
                                    nDblOut,
                                    dblOutNam,
                                    dblOutVal,
                                    nDblPar,
                                    dblParNam,
                                    dblParVal,
                                    resWri)
    annotation (Library={"CYMDISTToFMUPython34",  "python34"},
      LibraryDirectory={"modelica://CYMDISTToFMU.Resources/Library"},
      IncludeDirectory="modelica://CYMDISTToFMU.Resources/C-Sources",
      Include="#include \"python34Wrapper.c\"");
  annotation (Documentation(info="<html>
<p>
This function exchanges data with CymDist through its Python API.
See 
<a href=\"modelica://CYMDISTToFMU.Python34.UsersGuide\">
CYMDISTToFMU.Python34.UsersGuide</a>
for instructions, and 
<a href=\"modelica://CYMDISTToFMU.Python34.Functions.Examples\">
CYMDISTToFMU.Python34.Functions.Examples</a>
for examples.
</p>
</html>", revisions="<html>
<ul>
<li>
October 17, 2016, by Thierry S. Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
end cymdist;
