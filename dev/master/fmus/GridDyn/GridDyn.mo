within ;
model GridDyn "This model emulates a GridDyn model"

  Modelica.Blocks.Interfaces.RealOutput VMAG_A(start=0.0, unit="kV")
    "VMAG_A" annotation(Placement(transformation(extent={{100,78},{122,100}}),
        iconTransformation(extent={{100,78},{122,100}})));
  Modelica.Blocks.Interfaces.RealOutput VMAG_B(start=0.0, unit="kV")
    "VMAG_B" annotation(Placement(transformation(extent={{100,56},{122,78}}),
        iconTransformation(extent={{100,56},{122,78}})));
  Modelica.Blocks.Interfaces.RealOutput VMAG_C(start=0.0, unit="kV")
    "VMAG_C" annotation(Placement(transformation(extent={{100,34},{122,56}}),
        iconTransformation(extent={{100,34},{122,56}})));
  Modelica.Blocks.Interfaces.RealOutput P_A(start=0.0, unit="kW")
    "P_A" annotation(Placement(transformation(extent={{100,10},{122,32}})));
  Modelica.Blocks.Interfaces.RealOutput P_B(start=0.0, unit="kW")
    "P_B" annotation(Placement(transformation(extent={{100,-12},{122,10}}),
        iconTransformation(extent={{100,-12},{122,10}})));
  Modelica.Blocks.Interfaces.RealOutput P_C(start=0.0, unit="kW")
    "P_C" annotation(Placement(transformation(extent={{100,-34},{122,-12}}),
        iconTransformation(extent={{100,-34},{122,-12}})));
  Modelica.Blocks.Interfaces.RealOutput Q_A(start=0.0, unit="kvar")
    "Q_A" annotation(Placement(transformation(extent={{100,-56},{122,-34}}),
        iconTransformation(extent={{100,-56},{122,-34}})));
  Modelica.Blocks.Interfaces.RealOutput Q_B(start=0.0, unit="kvar")
    "Q_B" annotation(Placement(transformation(extent={{100,-78},{122,-56}}),
        iconTransformation(extent={{100,-78},{122,-56}})));
  Modelica.Blocks.Interfaces.RealOutput Q_C(start=0.0, unit="kvar")
    "Q_C" annotation(Placement(transformation(extent={{100,-100},{122,-78}}),
        iconTransformation(extent={{100,-100},{122,-78}})));
  Modelica.Blocks.Interfaces.RealInput voltage_A_HOLLISTER_2104( unit="V")
    "voltage_A" annotation(Placement(transformation(extent={{-120,30},{-100,50}})));
  Modelica.Blocks.Interfaces.RealInput voltage_B_HOLLISTER_2104( unit="V")
    "voltage_B" annotation(Placement(transformation(extent={{-120,-10},{-100,10}})));
  Modelica.Blocks.Interfaces.RealInput voltage_C_HOLLISTER_2104( unit="V")
    "voltage_C" annotation(Placement(transformation(extent={{-120,-50},{-100,
            -30}})));
  Modelica.Blocks.Sources.RealExpression con(y=7287)
    annotation (Placement(transformation(extent={{60,78},{80,98}})));
  Modelica.Blocks.Sources.RealExpression con1(y=7299)
    annotation (Placement(transformation(extent={{60,56},{80,76}})));
  Modelica.Blocks.Sources.RealExpression con2(y=7318)
    annotation (Placement(transformation(extent={{60,34},{80,54}})));
  Modelica.Blocks.Sources.RealExpression con3(y=7272)
    annotation (Placement(transformation(extent={{60,10},{80,30}})));
  Modelica.Blocks.Sources.RealExpression con4(y=2118)
    annotation (Placement(transformation(extent={{60,-10},{80,10}})));
  Modelica.Blocks.Sources.RealExpression con5(y=6719)
    annotation (Placement(transformation(extent={{60,-34},{80,-14}})));
  Modelica.Blocks.Sources.RealExpression con6(y=-284)
    annotation (Placement(transformation(extent={{60,-56},{80,-36}})));
  Modelica.Blocks.Sources.RealExpression con7(y=-7184)
    annotation (Placement(transformation(extent={{60,-78},{80,-58}})));
  Modelica.Blocks.Sources.RealExpression con8(y=3564)
    annotation (Placement(transformation(extent={{60,-98},{80,-78}})));
equation
  connect(con.y, VMAG_A)
    annotation (Line(points={{81,88},{111,88},{111,89}}, color={0,0,127}));
  connect(con1.y, VMAG_B) annotation (Line(points={{81,66},{86,66},{86,67},{111,
          67}}, color={0,0,127}));
  connect(con4.y, P_B)
    annotation (Line(points={{81,0},{111,0},{111,-1}}, color={0,0,127}));
  connect(con8.y, Q_C)
    annotation (Line(points={{81,-88},{111,-88},{111,-89}}, color={0,0,127}));
  connect(con2.y, VMAG_C)
    annotation (Line(points={{81,44},{111,44},{111,45}}, color={0,0,127}));
  connect(con3.y, P_A) annotation (Line(points={{81,20},{90,20},{90,21},{111,21}},
        color={0,0,127}));
  connect(P_C, con5.y) annotation (Line(points={{111,-23},{92,-23},{92,-24},{81,
          -24}}, color={0,0,127}));
  connect(Q_A, con6.y) annotation (Line(points={{111,-45},{94,-45},{94,-46},{81,
          -46}}, color={0,0,127}));
  connect(Q_B, con7.y)
    annotation (Line(points={{111,-67},{81,-67},{81,-68}}, color={0,0,127}));
  annotation (uses(Modelica(version="3.2.2")), Documentation(info="<html>
<p>This model has three inputs and nine outputs. </p>
<p>The inputs are not used in the model. </p>
<p>All the outputs are constant. The outputs names are </p>
<p style=\"margin-left: 30px;\">[&apos;VMAG_A&apos;, 
&apos;VMAG_B&apos;, &apos;VMAG_C&apos;, &apos;P_A&apos;, 
&apos;P_B&apos;, &apos;P_C&apos;, &apos;Q_A&apos;, 
&apos;Q_B&apos;, &apos;Q_C&apos;]. </p>
<p>The outputs values are</p>
<p style=\"margin-left: 30px;\">[7287, 7299, 7318, 7272, 2118, 6719, -284, -7184, 3564]. </p>
</html>"));
end GridDyn;
