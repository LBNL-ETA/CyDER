within ;
model DummyGridDyn "This model emulates a GridDyn model"

  Modelica.Blocks.Sources.RealExpression con(y=2520)
    annotation (Placement(transformation(extent={{60,32},{80,52}})));
  Modelica.Blocks.Sources.RealExpression con1(y=2520)
    annotation (Placement(transformation(extent={{60,12},{80,32}})));
  Modelica.Blocks.Sources.RealExpression con2(y=2520)
    annotation (Placement(transformation(extent={{60,-10},{80,10}})));
  Modelica.Blocks.Sources.RealExpression con3(y=0.0)
    annotation (Placement(transformation(extent={{60,-30},{80,-10}})));
  Modelica.Blocks.Sources.RealExpression con4(y=-120.0)
    annotation (Placement(transformation(extent={{60,-50},{80,-30}})));
  Modelica.Blocks.Sources.RealExpression con5(y=120.0)
    annotation (Placement(transformation(extent={{60,-70},{80,-50}})));
  Modelica.Blocks.Interfaces.RealInput KWA_800032440( unit="kW") "KWA"
          annotation(Placement(transformation(extent={{-120,82},{-100,102}})));
  Modelica.Blocks.Interfaces.RealInput KWB_800032440( unit="kW") "KWB"
          annotation(Placement(transformation(extent={{-120,46},{-100,66}})));
  Modelica.Blocks.Interfaces.RealInput KWC_800032440( unit="kW") "KWC"
          annotation(Placement(transformation(extent={{-120,10},{-100,30}})));
  Modelica.Blocks.Interfaces.RealInput KVARA_800032440( unit="kvar") "KVARA"
            annotation(Placement(transformation(extent={{-120,-26},{-100,-6}})));
  Modelica.Blocks.Interfaces.RealInput KVARB_800032440( unit="kvar") "KVARB"
            annotation(Placement(transformation(extent={{-120,-62},{-100,-42}})));
  Modelica.Blocks.Interfaces.RealOutput VMAG_A(start=0.0, unit="V") "VMAG_A"
             annotation(Placement(transformation(extent={{100,30},{122,52}})));
  Modelica.Blocks.Interfaces.RealOutput VMAG_B(start=0.0, unit="V") "VMAG_B"
             annotation(Placement(transformation(extent={{100,10},{122,32}})));
  Modelica.Blocks.Interfaces.RealOutput VMAG_C(start=0.0, unit="V") "VMAG_C"
             annotation(Placement(transformation(extent={{100,-10},{122,12}})));
  Modelica.Blocks.Interfaces.RealOutput VANG_A(start=0.0, unit="deg") "VANG_A"
             annotation(Placement(transformation(extent={{100,-30},{122,-8}})));
  Modelica.Blocks.Interfaces.RealOutput VANG_B(start=-120.0, unit="deg") "VANG_B"
             annotation(Placement(transformation(extent={{100,-50},{122,-28}})));
  Modelica.Blocks.Interfaces.RealOutput VANG_C(start=120.0, unit="deg") "VANG_C"
             annotation(Placement(transformation(extent={{100,-70},{122,-48}})));
  Modelica.Blocks.Interfaces.RealInput KVARC_800032440(unit="kvar") "KVARC"
    annotation (Placement(transformation(extent={{-122,-102},{-102,-82}})));
equation
  connect(con5.y, VANG_C) annotation (Line(points={{81,-60},{90,-60},{90,-59},{
          111,-59}}, color={0,0,127}));
  connect(con4.y, VANG_B) annotation (Line(points={{81,-40},{92,-40},{92,-39},{
          111,-39}}, color={0,0,127}));
  connect(con3.y, VANG_A) annotation (Line(points={{81,-20},{92,-20},{92,-19},{
          111,-19}}, color={0,0,127}));
  connect(con2.y, VMAG_C)
    annotation (Line(points={{81,0},{90,0},{90,1},{111,1}}, color={0,0,127}));
  connect(con1.y, VMAG_B) annotation (Line(points={{81,22},{94,22},{94,21},{111,
          21}}, color={0,0,127}));
  connect(con.y, VMAG_A) annotation (Line(points={{81,42},{92,42},{92,41},{111,
          41}}, color={0,0,127}));
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
end DummyGridDyn;
