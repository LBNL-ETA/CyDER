within ;
model DoubleInputDoubleOutput
  Modelica.Blocks.Interfaces.RealInput u
    annotation (Placement(transformation(extent={{-140,20},{-100,60}})));
  Modelica.Blocks.Interfaces.RealInput u1
    annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
  Modelica.Blocks.Interfaces.RealOutput y
    annotation (Placement(transformation(extent={{100,30},{120,50}})));
  Modelica.Blocks.Interfaces.RealOutput y1
    annotation (Placement(transformation(extent={{100,-50},{120,-30}})));
equation
  connect(u, y) annotation (Line(points={{-120,40},{-62,40},{-4,40},{110,40}},
        color={0,0,127}));
  connect(u1, y1) annotation (Line(points={{-120,-40},{110,-40},{110,-40}},
        color={0,0,127}));
  annotation (uses(Modelica(version="3.2.1")));
end DoubleInputDoubleOutput;
