within CYMDISTToFMU.Python34.Functions;
function cymdist "Function that communicates with the CYMDISTToFMU Python API"
  extends Modelica.Icons.Function;
  input String moduleName
  "Name of the python module that contains the function";
  input String functionName=moduleName "Name of the python function";
  input Real    modNamRef[1]  "Model name reference value";
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
  output Real dblOutVal[max(1, nDblOut)] "Double output values read from CYMDISTToFMU";
protected
  String pytPat "Value of PYTHONPATH environment variable";
  String pytPatCYMDISTToFMU "PYTHONPATH of CYMDISTToFMU library";
  Boolean havePytPat "true if PYTHONPATH is already set by the user";
  //--  String filNam = "file://Utilities/IO/Python34/UsersGuide/package.mo"
  //--    "Name to a file of the CYMDISTToFMU library";
algorithm
  // Get the directory to CYMDISTToFMU/Resources/Python-Sources
  //-- The lines below do not work in Dymola 2014 due to an issue with the loadResource
  //-- (ticket #15168). This will be fixed in future versions.
  //-- pytPatCYMDISTToFMU := CYMDISTToFMU.BoundaryConditions.WeatherData.BaseClasses.getAbsolutePath(uri=filNam);
  //-- pytPatCYMDISTToFMU := Modelica.Utilities.Strings.replace(
  //--   string=pytPatCYMDISTToFMU,
  //--   searchString=filNam,
  //--   replaceString="Resources/Python-Sources");
  // The next line is a temporary fix for the above problem
  pytPatCYMDISTToFMU := "Resources/Python-Sources";
  // Update the PYTHONPATH variable
  (
pytPat,havePytPat) := Modelica.Utilities.System.getEnvironmentVariable("PYTHONPATH");
  if havePytPat then
 Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH",
    content=pytPat + ":" + pytPatCYMDISTToFMU);
  else
 Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH",
    content=pytPatCYMDISTToFMU);
  end if;
  // Call the exchange function
dblOutVal := BaseClasses.cymdist(
      moduleName=moduleName,
      functionName=functionName,
      modNamRef=modNamRef,
      nDblInp=nDblInp,
      dblInpNam=dblInpNam,
      dblInpVal=dblInpVal,
      nDblOut=nDblOut,
      dblOutNam=dblOutNam,
      nDblPar=nDblPar,
      dblParNam=dblParNam,
      dblParVal=dblParVal,
      resWri=resWri);
  // Change the PYTHONPATH back to what it was so that the function has no
  // side effects.
  if havePytPat then
 Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH",
    content=pytPat);
  else
 Modelica.Utilities.System.setEnvironmentVariable(name="PYTHONPATH",
    content="");
  end if;
annotation (Documentation(info="<html>
<p>
This function is a wrapper for 
<a href=\"modelica://CYMDISTToFMU.Python34.Functions.BaseClasses.cymdist\">
CYMDISTToFMU.Python34.Functions.BaseClasses.cymdist</a>.
It adds the directory <code>modelica://CYMDISTToFMU/Resources/Python-Sources</code>
to the environment variable <code>PYTHONPATH</code>
prior to calling the function that exchanges data with Python.
After the function call, the <code>PYTHONPATH</code> is set back to what
it used to be when entering this function.
See 
<a href=\"modelica://CYMDISTToFMU.Python34.UsersGuide\">
CYMDISTToFMU.Python34.UsersGuide</a>
for instructions, and 
<a href=\"modelica://CYMDISTToFMU.Python34.Functions.Examples\">
CYMDISTToFMU.Python34.Functions.Examples</a>
for examples.
</p>
</html>",
        revisions="<html>
<ul>
<li>
October 17, 2016, by Thierry S. Nouidui:<br/>
First implementation.
</li>
</ul>
</html>"));
end cymdist;
