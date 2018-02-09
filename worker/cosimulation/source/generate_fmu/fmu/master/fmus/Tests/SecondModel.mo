within ;
model SecondModel

  Modelica.Blocks.Interfaces.RealInput u( start = -1.0)
    annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
  Modelica.Blocks.Interfaces.RealOutput y
    annotation (Placement(transformation(extent={{100,-10},{120,10}})));
  Modelica.Blocks.Sources.RealExpression realExpression(y=u*u)
    annotation (Placement(transformation(extent={{-12,-12},{14,12}})));
equation
  connect(realExpression.y, y)
    annotation (Line(points={{15.3,0},{56.5,0},{110,0}}, color={0,0,127}));
  annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
        coordinateSystem(preserveAspectRatio=false)),
    uses(Modelica(version="3.2.2")));
end SecondModel;
