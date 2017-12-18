within ;
package CyDER
  package HIL
    package Controls
      model voltvar

        Modelica.Blocks.Interfaces.RealInput v_pu "Voltage [p.u.]"
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
        Modelica.Blocks.Interfaces.RealOutput q_control "Q control signal"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        Modelica.Blocks.Interfaces.RealInput v_maxdead
          "Upper bound of deadband [p.u.]"
          annotation (Placement(transformation(extent={{-140,20},{-100,60}})));
        Modelica.Blocks.Interfaces.RealInput v_max "Voltage maximum [p.u.]"
          annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
        Modelica.Blocks.Interfaces.RealInput v_mindead
          "Upper bound of deadband [p.u.]"
          annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
        Modelica.Blocks.Interfaces.RealInput v_min "Voltage minimum [p.u.]"
          annotation (Placement(transformation(extent={{-140,-100},{-100,-60}})));
        Modelica.Blocks.Interfaces.RealInput q_max "Q control minimum (centered zero)" annotation (
            Placement(transformation(
              extent={{-20,-20},{20,20}},
              rotation=270,
              origin={20,120})));
        Modelica.Blocks.Interfaces.RealInput q_min "Q control maximum (centered zero)" annotation (
            Placement(transformation(
              extent={{-20,-20},{20,20}},
              rotation=270,
              origin={-40,120})));
      equation
        q_control = smooth(0,
          if v_pu > v_max then q_min
          elseif v_pu > v_maxdead then (v_maxdead - v_pu)/abs(v_max - v_maxdead) * q_max
          elseif v_pu < v_min then q_max
          elseif v_pu < v_mindead then (v_mindead - v_pu)/abs(v_min - v_mindead) * q_min * (-1)
          else 0);

      end voltvar;
    end Controls;

    package uPMU

      model uPMU_API
        Buildings.Utilities.IO.Python27.Real_Real Placeholder
          annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end uPMU_API;
    end uPMU;

    package Examples
      model Validate_VoltVarControl

        Modelica.Blocks.Sources.Ramp ramp(
          duration=1,
          startTime=0,
          height=0.2,
          offset=0.9)
          annotation (Placement(transformation(extent={{-90,-10},{-70,10}})));
        Modelica.Blocks.Sources.Constant upper_voltage(k=1.05)
          annotation (Placement(transformation(extent={{-60,50},{-40,70}})));
        Modelica.Blocks.Sources.Constant lower_voltage(k=0.95)
          annotation (Placement(transformation(extent={{-60,-70},{-40,-50}})));
        Controls.voltvar voltvar
          annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
        Modelica.Blocks.Sources.Constant upper_deadband_voltage(k=1.01)
          annotation (Placement(transformation(extent={{-60,10},{-40,30}})));
        Modelica.Blocks.Sources.Constant lower_deadband_voltage(k=0.99)
          annotation (Placement(transformation(extent={{-60,-30},{-40,-10}})));
        Modelica.Blocks.Sources.Constant upper_q(k=1) annotation (Placement(
              transformation(
              extent={{-10,-10},{10,10}},
              rotation=-90,
              origin={40,60})));
        Modelica.Blocks.Sources.Constant lower_q(k=-1) annotation (Placement(
              transformation(
              extent={{-10,-10},{10,10}},
              rotation=-90,
              origin={0,60})));
      equation
        connect(ramp.y, voltvar.v_pu)
          annotation (Line(points={{-69,0},{-12,0}}, color={0,0,127}));
        connect(lower_voltage.y, voltvar.v_min) annotation (Line(points={{-39,
                -60},{-20,-60},{-20,-8},{-12,-8}}, color={0,0,127}));
        connect(upper_voltage.y, voltvar.v_max) annotation (Line(points={{-39,
                60},{-20,60},{-20,8},{-12,8}}, color={0,0,127}));
        connect(voltvar.v_mindead, lower_deadband_voltage.y) annotation (Line(
              points={{-12,-4},{-30,-4},{-30,-20},{-39,-20}}, color={0,0,127}));
        connect(upper_deadband_voltage.y, voltvar.v_maxdead) annotation (Line(
              points={{-39,20},{-30,20},{-30,4},{-12,4}}, color={0,0,127}));
        connect(lower_q.y, voltvar.q_min) annotation (Line(points={{
                -1.9984e-015,49},{0,49},{0,30},{-4,30},{-4,12}}, color={0,0,127}));
        connect(upper_q.y, voltvar.q_max) annotation (Line(points={{40,49},{40,
                49},{40,40},{12,40},{12,20},{2,20},{2,12}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Validate_VoltVarControl;
    end Examples;
  end HIL;

  package Optimization
    package Examples

      model Test_voltage
      protected
        parameter Modelica.SIunits.Impedance Z11_601[2] = {0.3465, 1.0179};
        parameter Modelica.SIunits.Impedance Z12_601[2] = {0.1560, 0.5017};
        parameter Modelica.SIunits.Impedance Z13_601[2] = {0.1580, 0.4236};
        parameter Modelica.SIunits.Impedance Z22_601[2] = {0.3375, 1.0478};
        parameter Modelica.SIunits.Impedance Z23_601[2] = {0.1535, 0.3849};
        parameter Modelica.SIunits.Impedance Z33_601[2] = {0.3414, 1.0348};
      public
        parameter Real capctrl=1;
        Modelica.Blocks.Sources.Ramp ramp_incuctor(
          duration=1,
          startTime=1,
          offset=0.99,
          height=-0.98)
          annotation (Placement(transformation(extent={{100,20},{80,40}})));
        Buildings.Electrical.AC.ThreePhasesUnbalanced.Sources.FixedVoltage source1(
                                                                                  f=60, V=4.16e3)
                   annotation (Placement(transformation(extent={{-100,-10},{-80,10}})));
        Buildings.Electrical.AC.ThreePhasesUnbalanced.Loads.Inductive inductor(
          loadConn=Buildings.Electrical.Types.LoadConnection.wye_to_wyeg,
          mode=Buildings.Electrical.Types.Load.FixedZ_steady_state,
          V_nominal=4.16e3,
          use_pf_in=true,
          pf=0.005,
          P_nominal=-1000)
          annotation (Placement(transformation(extent={{40,30},{60,50}})));
        Chargepoint.Simulation.Components.Probe
                         sens_inductor
          annotation (Placement(transformation(extent={{0,30},{20,50}})));
        Chargepoint.Simulation.Components.Probe
                         sens_head
          annotation (Placement(transformation(extent={{-40,-10},{-20,10}})));
        Buildings.Electrical.AC.ThreePhasesUnbalanced.Lines.TwoPortMatrixRL line_650(
          Z11=2000/5280*Z11_601,
          Z12=2000/5280*Z12_601,
          Z13=2000/5280*Z13_601,
          Z22=2000/5280*Z22_601,
          Z23=2000/5280*Z23_601,
          Z33=2000/5280*Z33_601,
          V_nominal=4.16e3) annotation (Placement(transformation(
              extent={{-10,-10},{10,10}},
              rotation=0,
              origin={-50,0})));
        Chargepoint.Simulation.Components.Probe
                         sens_test
          annotation (Placement(transformation(extent={{-80,-10},{-60,10}})));
        Buildings.Electrical.AC.ThreePhasesUnbalanced.Loads.Capacitive capacitor(
          loadConn=Buildings.Electrical.Types.LoadConnection.wye_to_wyeg,
          mode=Buildings.Electrical.Types.Load.FixedZ_steady_state,
          V_nominal=1.16e3,
          use_pf_in=true,
          P_nominal=-1000,
          pf=0.005)
          annotation (Placement(transformation(extent={{40,-10},{60,10}})));
        Chargepoint.Simulation.Components.Probe
                         sens_capacitor
          annotation (Placement(transformation(extent={{0,-10},{20,10}})));
        Modelica.Blocks.Math.Gain gain(k=capctrl)
          annotation (Placement(transformation(extent={{0,-50},{20,-30}})));
        Modelica.Blocks.Sources.Constant const(k=1)
          annotation (Placement(transformation(extent={{-60,-50},{-40,-30}})));
        Modelica.Blocks.Interfaces.RealInput u
          annotation (Placement(transformation(extent={{30,-64},{70,-24}})));
      equation
        connect(sens_inductor.terminal_n,sens_head. terminal_p) annotation (Line(
              points={{0,40},{-10,40},{-10,0},{-20,0}}, color={0,120,120}));
        connect(sens_inductor.terminal_p,inductor. terminal)
          annotation (Line(points={{20,40},{40,40}}, color={0,120,120}));
        connect(ramp_incuctor.y,inductor. pf_in_3)
          annotation (Line(points={{79,30},{56.2,30}}, color={0,0,127}));
        connect(ramp_incuctor.y,inductor. pf_in_2)
          annotation (Line(points={{79,30},{64.5,30},{50,30}}, color={0,0,127}));
        connect(ramp_incuctor.y,inductor. pf_in_1)
          annotation (Line(points={{79,30},{44,30}}, color={0,0,127}));
        connect(sens_head.terminal_n,line_650. terminal_p)
          annotation (Line(points={{-40,0},{-40,0}}, color={0,120,120}));
        connect(source1.terminal,sens_test. terminal_n)
          annotation (Line(points={{-80,0},{-80,0}}, color={0,120,120}));
        connect(sens_test.terminal_p,line_650. terminal_n)
          annotation (Line(points={{-60,0},{-60,0}}, color={0,120,120}));
        connect(sens_capacitor.terminal_p,capacitor. terminal)
          annotation (Line(points={{20,0},{30,0},{40,0}}, color={0,120,120}));
        connect(sens_capacitor.terminal_n, sens_head.terminal_p)
          annotation (Line(points={{0,0},{-20,0}}, color={0,120,120}));
        connect(capacitor.pf_in_2, capacitor.pf_in_1) annotation (Line(points={{50,-10},
                {48,-10},{44,-10}},          color={0,0,127}));
        connect(capacitor.pf_in_3, capacitor.pf_in_2)
          annotation (Line(points={{56,-10},{50,-10}},          color={0,0,127}));
        connect(const.y, gain.u)
          annotation (Line(points={{-39,-40},{-20,-40},{-2,-40}}, color={0,0,127}));
        connect(capacitor.pf_in_2, u) annotation (Line(points={{50,-10},{54,-10},
                {54,-44},{50,-44}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Test_voltage;

      model Test_simple
        parameter Real capctrl=1;
        Modelica.Blocks.Math.Gain gain(k=capctrl)
          annotation (Placement(transformation(extent={{-20,40},{0,60}})));
        Modelica.Blocks.Interfaces.RealInput u
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
        Modelica.Blocks.Interfaces.RealOutput y
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        Modelica.Blocks.Math.Add add
          annotation (Placement(transformation(extent={{20,-10},{40,10}})));
        Modelica.Blocks.Sources.Sine sine(amplitude=1, freqHz=2)
          annotation (Placement(transformation(extent={{-60,40},{-40,60}})));
      equation
        connect(add.y, y)
          annotation (Line(points={{41,0},{110,0},{110,0}}, color={0,0,127}));
        connect(add.u1, gain.y)
          annotation (Line(points={{18,6},{10,6},{10,50},{1,50}}, color={0,0,127}));
        connect(add.u2, u) annotation (Line(points={{18,-6},{-44,-6},{-44,0},{-120,0}},
              color={0,0,127}));
        connect(sine.y, gain.u) annotation (Line(points={{-39,50},{-30,50},{-22,
                50}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Test_simple;
    end Examples;
  end Optimization;
  annotation (uses(Modelica(version="3.2.2"), Buildings(version="4.0.0")));
end CyDER;