within ;
model HVAC "Model of an ideal HVAC system which uses
  a PI controller to compute the load required to maintain
  the temperature set point defined by TRooSP"
  parameter Real TRooSP = 273.15 + 20
    "Room set point temperature in Kelvin";
  parameter Real kGai = 2e4
    "Proportional gain";
  Modelica.Blocks.Continuous.LimPID PI(
    controllerType=Modelica.Blocks.Types.SimpleController.PI,
    k=0.1,
    Ti=300,
    initType=Modelica.Blocks.Types.InitPID.InitialState)
    annotation (Placement(transformation(extent={{-30,10},{-10,30}})));
  Modelica.Blocks.Math.Gain gain(k=kGai)
    annotation (Placement(transformation(extent={{18,10},{38,30}})));
  Modelica.Blocks.Sources.Constant const(k=TRooSP)
    "Set point temperature"
    annotation (Placement(transformation(extent={{-94,30},{-74,50}})));
  Modelica.Blocks.Interfaces.RealInput TRoo
    "Room temperature in C"
    annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
  Modelica.Blocks.Math.UnitConversions.From_degC from_degC
    annotation (Placement(transformation(extent={{-78,-10},{-58,10}})));
  Modelica.Blocks.Interfaces.RealOutput Q "Load"
    annotation (Placement(transformation(extent={{100,-10},{120,10}})));
equation
  connect(gain.u, PI.y)
    annotation (Line(points={{16,20},{0,20},{-9,20}},
                                             color={0,0,127}));
  connect(const.y, PI.u_s)
    annotation (Line(points={{-73,40},{-74,40},{-60,40},{-60,20},{-32,20}},
                                                       color={0,0,127}));
  connect(from_degC.u, TRoo)
    annotation (Line(points={{-80,0},{-90,0},{-120,0}}, color={0,0,127}));
  connect(from_degC.y, PI.u_m)
    annotation (Line(points={{-57,0},{-20,0},{-20,8}}, color={0,0,127}));
  connect(gain.y, Q) annotation (Line(points={{39,20},{50,20},{60,20},{60,0},{110,
          0}}, color={0,0,127}));
  annotation (uses(Modelica(version="3.2.2")));
end HVAC;
