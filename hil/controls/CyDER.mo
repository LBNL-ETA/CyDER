within ;
package CyDER
  package HIL
    package Controls
      model voltVar

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
        Modelica.Blocks.Interfaces.RealInput q_maxind "Maximal Reactive Power (Inductive)" annotation (
            Placement(transformation(
              extent={{-20,-20},{20,20}},
              rotation=270,
              origin={20,120})));
        Modelica.Blocks.Interfaces.RealInput q_maxcap "Maximal Reactive Power (Capacitive)" annotation (
            Placement(transformation(
              extent={{-20,-20},{20,20}},
              rotation=270,
              origin={-40,120})));
      equation
        q_control = smooth(0,
          if v_pu > v_max then q_maxind * (-1)
          elseif v_pu > v_maxdead then (v_maxdead - v_pu)/abs(v_max - v_maxdead) * q_maxind
          elseif v_pu < v_min then q_maxcap
          elseif v_pu < v_mindead then (v_mindead - v_pu)/abs(v_min - v_mindead) * q_maxcap
          else 0);
      end voltVar;

      model voltVar_param

        Modelica.Blocks.Interfaces.RealInput v(unit="1") "Voltage [p.u]"
          annotation (Placement(transformation(extent={{-140,-20},{-100,20}})));
        Modelica.Blocks.Interfaces.RealOutput QCon(unit="kvar") "Q control signal"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        parameter Real thr(start=0.05) "over/undervoltage threshold";
        parameter Real hys(start=0.01) "Hysteresis";
        final parameter Modelica.SIunits.PerUnit vMaxDea=1 + hys "Upper bound of deaband [p.u.]";
        final parameter Modelica.SIunits.PerUnit vMax=1 + thr "Voltage maximum [p.u.]";
        final parameter Modelica.SIunits.PerUnit vMinDea=1 - hys "Upper bound of deaband [p.u.]";
        final parameter Modelica.SIunits.PerUnit vMin=1 - thr "Voltage minimum [p.u.]";
        parameter Real QMaxInd(start=1.0, unit="kvar") "Maximal Reactive Power (Inductive)";
        parameter Real QMaxCap(start=1.0, unit="kvar") "Maximal Reactive Power (Capacitive)";
      equation
        QCon = smooth(0, if v > vMax then QMaxInd*(-1) elseif v > vMaxDea then (vMaxDea - v)/
          abs(vMax - vMaxDea)*QMaxInd elseif v < vMin then QMaxCap elseif v < vMinDea then (
          vMinDea - v)/abs(vMin - vMinDea)*QMaxCap else 0);
        annotation (Documentation(info="<html>
This model is similar to <a href=\"modelica://CyDER.HIL.Controls.voltVar\">
CyDER.HIL.Controls.voltVar</a> 
with the only differences that input variables have been 
changed to parameters.
</html>"));
      end voltVar_param;
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
        Controls.voltVar voltVar
          annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
        Modelica.Blocks.Sources.Constant upper_deadband_voltage(k=1.01)
          annotation (Placement(transformation(extent={{-60,10},{-40,30}})));
        Modelica.Blocks.Sources.Constant lower_deadband_voltage(k=0.99)
          annotation (Placement(transformation(extent={{-60,-30},{-40,-10}})));
        Modelica.Blocks.Sources.Constant qmax_inductive(k=1) annotation (Placement(
              transformation(
              extent={{-10,-10},{10,10}},
              rotation=-90,
              origin={40,60})));
        Modelica.Blocks.Sources.Constant qmax_capacitive(k=0.2) annotation (Placement(
              transformation(
              extent={{-10,-10},{10,10}},
              rotation=-90,
              origin={0,60})));
      equation
        connect(ramp.y, voltVar.v_pu)
          annotation (Line(points={{-69,0},{-12,0}}, color={0,0,127}));
        connect(lower_voltage.y, voltVar.v_min) annotation (Line(points={{-39,
                -60},{-20,-60},{-20,-8},{-12,-8}}, color={0,0,127}));
        connect(upper_voltage.y, voltVar.v_max) annotation (Line(points={{-39,
                60},{-20,60},{-20,8},{-12,8}}, color={0,0,127}));
        connect(voltVar.v_mindead, lower_deadband_voltage.y) annotation (Line(
              points={{-12,-4},{-30,-4},{-30,-20},{-39,-20}}, color={0,0,127}));
        connect(upper_deadband_voltage.y, voltVar.v_maxdead) annotation (Line(
              points={{-39,20},{-30,20},{-30,4},{-12,4}}, color={0,0,127}));
        connect(qmax_capacitive.y, voltVar.q_maxcap) annotation (Line(points={{-1.9984e-015,
                49},{0,49},{0,30},{-4,30},{-4,12}}, color={0,0,127}));
        connect(qmax_inductive.y, voltVar.q_maxind) annotation (Line(points={{40,49},{40,
                49},{40,40},{12,40},{12,20},{2,20},{2,12}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Validate_VoltVarControl;

      model Validate_VoltVarControl_param

        Modelica.Blocks.Sources.Ramp ramp(
          duration=1,
          startTime=0,
          height=0.2,
          offset=0.9)
          annotation (Placement(transformation(extent={{-90,-10},{-70,10}})));
        Controls.voltVar_param voltVar_param(QMaxCap=0.5)
          annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
      equation
        connect(voltVar_param.v, ramp.y)
          annotation (Line(points={{-12,0},{-69,0}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Validate_VoltVarControl_param;
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

  package PvModel
    package Examples
    end Examples;

    package Models
      model PvOrientated
        parameter Real A_PV=1 "Area of PV system";
        parameter Real til=10 "Surface tilt [deg]";
        parameter Real azi=0 "Surface azimuth [deg]";

        Buildings.BoundaryConditions.WeatherData.ReaderTMY3
                                                  weaDat(
            computeWetBulbTemperature=false, filNam=
              "C:/Users/Christoph/Documents/GitHub/cyder/hil/controls/USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos")
          "Weather data model"
          annotation (Placement(transformation(extent={{-60,20},{-40,40}})));
        Buildings.Electrical.AC.ThreePhasesBalanced.Sources.PVSimpleOriented
                                                        pv1(
          eta_DCAC=0.89,
          A=A_PV,
          fAct=0.9,
          eta=0.12,
          linearized=false,
          pf=1,
          lat=weaDat.lat,
          azi=Modelica.SIunits.Conversions.from_deg(azi),
          til=Modelica.SIunits.Conversions.from_deg(til),
          V_nominal=120)       "PV"
          annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
        Modelica.Blocks.Interfaces.RealOutput Power(unit="W") "Generated power"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        Buildings.Electrical.AC.ThreePhasesBalanced.Sources.FixedVoltage fixVol(V=120, f=60)
          annotation (Placement(transformation(extent={{-60,-10},{-40,10}})));
      equation
        connect(weaDat.weaBus, pv1.weaBus) annotation (Line(
            points={{-40,30},{0,30},{0,9}},
            color={255,204,51},
            thickness=0.5));
        connect(pv1.P, Power) annotation (Line(points={{11,7},{20.5,7},{20.5,0},{110,0}},
              color={0,0,127}));
        connect(fixVol.terminal, pv1.terminal)
          annotation (Line(points={{-40,0},{-10,0}}, color={0,120,120}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end PvOrientated;
    end Models;
  end PvModel;
  annotation (uses(Modelica(version="3.2.2"), Buildings(version="4.0.0")));
end CyDER;
