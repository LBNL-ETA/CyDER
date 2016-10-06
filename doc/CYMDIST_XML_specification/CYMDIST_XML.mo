within ;
model CYMDIST_XML
  "Input data for a CYMDIST FMU. This model is used to
  generate the xml which will be modified, and use as
  input for CYMDISTPY."
  parameter Real par1( unit="Ohm") = 1.0
    "First parameter";
  parameter Real par2( unit="Ohm") = 10.0
    "Second parameter";
  Modelica.Blocks.Interfaces.RealInput u(
    start=1.0, unit="A") "First input"
    annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
  Modelica.Blocks.Interfaces.RealOutput y(
    unit="V") "First output"
    annotation (Placement(transformation(extent={{100,10},{120,30}})));
  Modelica.Blocks.Interfaces.RealInput u1(
    start=2.0, unit="A") "Second input"
    annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
  Modelica.Blocks.Interfaces.RealOutput y1(
    unit = "V") "Second output"
    annotation (Placement(transformation(extent={{100,70},{120,90}})));
protected
  Modelica.Blocks.Math.Gain gain(k(unit="Ohm")=par1)
    annotation (Placement(transformation(extent={{-4,
            70},{16,90}})));
  Modelica.Blocks.Math.Gain gain1(k(unit="Ohm")=par2)
    annotation (Placement(transformation(extent={{-4,
            10},{16,30}})));
equation
  connect(gain.u, u1) annotation (Line(points={{-6,80},
          {-120,80}}, color={0,0,127}));
  connect(gain.y, y1) annotation (Line(points={{17,80},
          {110,80}}, color={0,0,127}));
  connect(u, gain1.u) annotation (Line(points={{-120,
          20},{-64,20},{-6,20}}, color={0,0,127}));
  connect(gain1.y, y) annotation (Line(points={{17,20},
          {64,20},{110,20}}, color={0,0,127}));
  annotation (uses(Modelica(version="3.2.2")));
end CYMDIST_XML;
