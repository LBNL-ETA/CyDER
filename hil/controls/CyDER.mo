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

      model voltVar_param_noEvents
        function actuate
        input Real v
                    "Voltage [p.u]";
        input Real thr
                      "over/undervoltage threshold";
        input Real hys
                      "Hysteresis";
        input Modelica.SIunits.PerUnit vMaxDea "Upper bound of deaband [p.u.]";
        input Modelica.SIunits.PerUnit vMax "Voltage maximum [p.u.]";
        input Modelica.SIunits.PerUnit vMinDea "Upper bound of deaband [p.u.]";
        input Modelica.SIunits.PerUnit vMin "Voltage minimum [p.u.]";
        input Real QMaxInd "Maximal Reactive Power (Inductive)";
        input Real QMaxCap
                          "Maximal Reactive Power (Capacitive)";
        output Real QCon;
        algorithm
        QCon := smooth(0, if v > vMax then QMaxInd*(-1) elseif v > vMaxDea then (vMaxDea - v)/
          abs(vMax - vMaxDea)*QMaxInd elseif v < vMin then QMaxCap elseif v < vMinDea then (
          vMinDea - v)/abs(vMin - vMinDea)*QMaxCap else 0);
        end actuate;

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
        QCon = actuate(v,thr, hys, vMaxDea, vMax, vMinDea, vMin, QMaxInd, QMaxCap);
        annotation (Documentation(info="<html>
This model is similar to <a href=\"modelica://CyDER.HIL.Controls.voltVar\">
CyDER.HIL.Controls.voltVar</a> 
with the only differences that input variables have been 
changed to parameters.
</html>"));
      end voltVar_param_noEvents;
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

      model Validate_VoltVarControl_param_noEvents

        Modelica.Blocks.Sources.Ramp ramp(
          duration=1,
          startTime=0,
          height=0.2,
          offset=0.9)
          annotation (Placement(transformation(extent={{-90,-10},{-70,10}})));
        Controls.voltVar_param_noEvents voltVar_param_noEvents(QMaxCap=0.5)
          annotation (Placement(transformation(extent={{-10,-10},{10,10}})));
      equation
        connect(voltVar_param.v, ramp.y)
          annotation (Line(points={{-12,0},{-69,0}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Validate_VoltVarControl_param_noEvents;
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
    package Models
      model PV_simple_tilted "Simple PV model based on irradiation"
        parameter Modelica.SIunits.Area A(min=0) = 1 "Net surface area";
        parameter Real eta(min=0, max=1, unit="1") = 0.9*0.12*0.9
          "Module conversion efficiency";
        parameter Real lat=37.9 "Latitude [deg]";
        parameter Real til=10 "Surface tilt [deg]";
        parameter Real azi=0 "Surface azimuth [deg]";
        Modelica.Blocks.Interfaces.RealInput Shading(min=0, max=1, unit="1")
          "Shading of PV module"
          annotation (Placement(transformation(
              origin={-120,-40},
              extent={{20,20},{-20,-20}},
              rotation=180), iconTransformation(
              extent={{-20,-20},{20,20}},
              rotation=0,
              origin={-120,-40})));
        Modelica.Blocks.Interfaces.RealOutput PV_generation "PV generation"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        Tilted_Solar_TMY                           tilted_Solar_TMY(
          til=til,
          lat=lat,
          azi=azi) annotation (Placement(transformation(extent={{-68,-10},{-48,10}})));
        Buildings.BoundaryConditions.WeatherData.Bus
                        weaBus "Bus with weather data"
          annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
      equation
        PV_generation = A * eta * tilted_Solar_TMY.G * (1 - Shading);
        connect(weaBus, tilted_Solar_TMY.weaBus) annotation (Line(
            points={{-100,0},{-84,0},{-68,0}},
            color={255,204,51},
            thickness=0.5), Text(
            string="%first",
            index=-1,
            extent={{-6,3},{-6,3}}));
      end PV_simple_tilted;

      model Tilted_Solar_TMY
        parameter Real lat=37.9 "Latitude [deg]";
        parameter Real til=0 "Surface tilt [deg]";
        parameter Real azi=0 "Surface azimuth [deg]";
        Solar.DiffusePerez HDifTil(
          azi=Modelica.SIunits.Conversions.from_deg(azi),
          til=Modelica.SIunits.Conversions.from_deg(til),
          lat=Modelica.SIunits.Conversions.from_deg(lat))
          "Diffuse irradiation on tilted surface"
          annotation (Placement(transformation(extent={{-20,10},{0,30}})));
        Solar.DirectTiltedSurface HDirTil(
          azi=Modelica.SIunits.Conversions.from_deg(azi),
          til=Modelica.SIunits.Conversions.from_deg(til),
          lat=Modelica.SIunits.Conversions.from_deg(lat))
          "Direct irradiation on tilted surface"
          annotation (Placement(transformation(extent={{-20,-30},{0,-10}})));
        Modelica.Blocks.Math.Add sum "Total irradiation on tilted surface"
          annotation (Placement(transformation(
              extent={{10,-10},{-10,10}},
              rotation=180,
              origin={50,0})));
        Modelica.Blocks.Interfaces.RealOutput G(final quantity="RadiantEnergyFluenceRate",
            final unit="W/m2") "Tilted Solar Radiation"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
        Buildings.BoundaryConditions.WeatherData.Bus
                        weaBus "Bus with weather data"
          annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
      equation
        connect(sum.u2, HDifTil.H)
          annotation (Line(points={{38,6},{20,6},{20,20},{1,20}}, color={0,0,127}));
        connect(sum.u1, HDirTil.H) annotation (Line(points={{38,-6},{20,-6},{20,-20},{
                1,-20}}, color={0,0,127}));
        connect(sum.y, G) annotation (Line(points={{61,0},{110,0}}, color={0,0,127}));
        connect(HDifTil.weaBus, weaBus) annotation (Line(
            points={{-20,20},{-60,20},{-60,0},{-100,0}},
            color={255,204,51},
            thickness=0.5), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        connect(HDirTil.weaBus, weaBus) annotation (Line(
            points={{-20,-20},{-60,-20},{-60,0},{-100,0}},
            color={255,204,51},
            thickness=0.5), Text(
            string="%second",
            index=1,
            extent={{6,3},{6,3}}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Tilted_Solar_TMY;

      model PvOrientated_FMU
        parameter Real A_PV=1 "Area of PV system [m2]";
        parameter Real til=10 "Surface tilt [deg]";
        parameter Real azi=0 "Surface azimuth [deg]";
        parameter String filNam="" "Full path to weatherfile";
        Buildings.BoundaryConditions.WeatherData.ReaderTMY3
                                                  weaDat(
            computeWetBulbTemperature=false, filNam=
              filNam)
          "Weather data model"
          annotation (Placement(transformation(extent={{-80,-10},{-60,10}})));
        CyDER.PvModel.Models.PV_simple_tilted pV_cyder(
          lat=Modelica.SIunits.Conversions.to_deg(weaDat.lat),
          A=A_PV,
          til=til,
          azi=azi) annotation (Placement(transformation(extent={{-8,-10},{12,10}})));
        Modelica.Blocks.Sources.Constant shading(k=0)
          annotation (Placement(transformation(extent={{-44,-24},{-36,-16}})));
        Modelica.Blocks.Interfaces.RealOutput PV_generation "PV generation"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
      equation
        connect(shading.y, pV_cyder.Shading) annotation (Line(points={{-35.6,-20},{-20,
                -20},{-20,-4},{-10,-4}}, color={0,0,127}));
        connect(pV_cyder.weaBus, weaDat.weaBus) annotation (Line(
            points={{-8,0},{-30,0},{-60,0}},
            color={255,204,51},
            thickness=0.5));
        connect(pV_cyder.PV_generation, PV_generation)
          annotation (Line(points={{13,0},{110,0},{110,0}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end PvOrientated_FMU;
    end Models;

    package Examples
      model PvOrientated_ValidateModels
        parameter Real A_PV=1 "Area of PV system";
        parameter Real til=65 "Surface tilt [deg]";
        parameter Real azi=25 "Surface azimuth [deg]";
        parameter String filNam="C:/Users/Christoph/Documents/GitHub/cyder/hil/controls/USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos";
        //parameter String filNam="USA_CA_San.Francisco.Intl.AP.724940_TMY3.mos";
        Buildings.BoundaryConditions.WeatherData.ReaderTMY3
                                                  weaDat(
            computeWetBulbTemperature=false, filNam=
              filNam)
          "Weather data model"
          annotation (Placement(transformation(extent={{-80,-10},{-60,10}})));
        Buildings.Electrical.AC.OnePhase.Sources.PVSimpleOriented pv_buildings(
          pf=1,
          V_nominal=120,
          A=A_PV,
          azi=Modelica.SIunits.Conversions.from_deg(azi),
          til=Modelica.SIunits.Conversions.from_deg(til),
          lat=weaDat.lat)
          annotation (Placement(transformation(extent={{0,20},{20,40}})));
        Buildings.Electrical.AC.OnePhase.Sources.FixedVoltage fixVol(f=60, V=120)
          annotation (Placement(transformation(extent={{-20,20},{-12,28}})));
        CyDER.PvModel.Models.PV_simple_tilted pV_cyder(
          lat=Modelica.SIunits.Conversions.to_deg(weaDat.lat),
          A=A_PV,
          til=til,
          azi=azi) annotation (Placement(transformation(extent={{0,-100},{20,-80}})));
        Modelica.Blocks.Sources.Constant shading(k=0)
          annotation (Placement(transformation(extent={{-20,-100},{-12,-92}})));
      protected
        Buildings.BoundaryConditions.SolarIrradiation.DiffusePerez HDifTil_buildings(
          final til=Modelica.SIunits.Conversions.from_deg(til),
          final lat=weaDat.lat,
          final azi=Modelica.SIunits.Conversions.from_deg(azi)) "Diffuse irradiation on tilted surface"
          annotation (Placement(transformation(extent={{0,80},{20,100}})));
        Buildings.BoundaryConditions.SolarIrradiation.DirectTiltedSurface HDirTil_buildings(
          final til=Modelica.SIunits.Conversions.from_deg(til),
          final lat=weaDat.lat,
          final azi=Modelica.SIunits.Conversions.from_deg(azi)) "Direct irradiation on tilted surface"
          annotation (Placement(transformation(extent={{0,49},{20,69}})));
      public
        Solar.DiffusePerez HDifTil_cyder(
          azi=Modelica.SIunits.Conversions.from_deg(azi),
          til=Modelica.SIunits.Conversions.from_deg(til),
          lat=weaDat.lat) "Diffuse irradiation on tilted surface"
          annotation (Placement(transformation(extent={{0,-40},{20,-20}})));
        Solar.DirectTiltedSurface HDirTil_cyder(
          azi=Modelica.SIunits.Conversions.from_deg(azi),
          til=Modelica.SIunits.Conversions.from_deg(til),
          lat=weaDat.lat) "Direct irradiation on tilted surface"
          annotation (Placement(transformation(extent={{0,-70},{20,-50}})));
      protected
        Modelica.Blocks.Math.Gain gain_DCAC(final k=0.9)
          "Gain that represents the DCAC conversion losses"
          annotation (Placement(
              transformation(
              extent={{10,-10},{-10,10}},
              rotation=180,
              origin={50,30})));
      equation
        connect(shading.y, pV_cyder.Shading) annotation (Line(points={{-11.6,-96},{-8,
                -96},{-8,-94},{-2,-94}}, color={0,0,127}));
        connect(fixVol.terminal, pv_buildings.terminal) annotation (Line(points={{-12,
                24},{-8,24},{-8,30},{0,30}}, color={0,120,120}));
        connect(weaDat.weaBus, HDifTil_buildings.weaBus) annotation (Line(
            points={{-60,0},{-30,0},{-30,90},{0,90}},
            color={255,204,51},
            thickness=0.5));
        connect(weaDat.weaBus, HDirTil_buildings.weaBus) annotation (Line(
            points={{-60,0},{-30,0},{-30,59},{0,59}},
            color={255,204,51},
            thickness=0.5));
        connect(weaDat.weaBus, pv_buildings.weaBus) annotation (Line(
            points={{-60,0},{-30,0},{-30,39},{10,39}},
            color={255,204,51},
            thickness=0.5));
        connect(HDifTil_cyder.weaBus, weaDat.weaBus) annotation (Line(
            points={{0,-30},{-30,-30},{-30,0},{-60,0}},
            color={255,204,51},
            thickness=0.5));
        connect(HDirTil_cyder.weaBus, weaDat.weaBus) annotation (Line(
            points={{0,-60},{-30,-60},{-30,0},{-60,0}},
            color={255,204,51},
            thickness=0.5));
        connect(pV_cyder.weaBus, weaDat.weaBus) annotation (Line(
            points={{0,-90},{-30,-90},{-30,0},{-60,0}},
            color={255,204,51},
            thickness=0.5));
        connect(pv_buildings.P, gain_DCAC.u) annotation (Line(points={{21,37},{
                29.5,37},{29.5,30},{38,30}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end PvOrientated_ValidateModels;
    end Examples;
  end PvModel;

  package Solar
    block DiffusePerez
      "Hemispherical diffuse irradiation on a tilted surface using Perez's anisotropic sky model"
      extends
        Buildings.BoundaryConditions.SolarIrradiation.BaseClasses.PartialSolarIrradiation;
      parameter Real rho(min=0, max=1, final unit="1")=0.2 "Ground reflectance";
      parameter Modelica.SIunits.Angle lat "Latitude";
      parameter Modelica.SIunits.Angle azi "Surface azimuth";
      parameter Boolean outSkyCon=false
        "Output contribution of diffuse irradiation from sky";
      parameter Boolean outGroCon=false
        "Output contribution of diffuse irradiation from ground";
      Modelica.Blocks.Math.Add add "Block to add radiations"
        annotation (Placement(transformation(extent={{60,-10},{80,10}})));
      Modelica.Blocks.Interfaces.RealOutput HSkyDifTil if outSkyCon
        "Hemispherical diffuse solar irradiation on a tilted surface from the sky"
        annotation (Placement(transformation(extent={{100,50},{120,70}})));
      Modelica.Blocks.Interfaces.RealOutput HGroDifTil if outGroCon
        "Hemispherical diffuse solar irradiation on a tilted surface from the ground"
        annotation (Placement(transformation(extent={{100,-70},{120,-50}})));
    protected
      DiffusePerez_sub HDifTil(final til=til, final rho=rho)
        "Diffuse irradiation on tilted surface"
        annotation (Placement(transformation(extent={{0,-21},{42,21}})));
      Buildings.BoundaryConditions.SolarIrradiation.BaseClasses.SkyClearness skyCle
        "Sky clearness"
        annotation (Placement(transformation(extent={{-62,16},{-54,24}})));
      Buildings.BoundaryConditions.SolarIrradiation.BaseClasses.BrighteningCoefficient
        briCoe "Brightening coefficient"
        annotation (Placement(transformation(extent={{-40,-34},{-32,-26}})));
      Buildings.BoundaryConditions.SolarIrradiation.BaseClasses.RelativeAirMass relAirMas
        "Relative air mass"
        annotation (Placement(transformation(extent={{-80,-44},{-72,-36}})));
      Buildings.BoundaryConditions.SolarIrradiation.BaseClasses.SkyBrightness skyBri
        "Sky brightness"
        annotation (Placement(transformation(extent={{-60,-54},{-52,-46}})));
      IncidenceAngle incAng(
        lat=lat,
        azi=azi,
        til=til) "Incidence angle"
        annotation (Placement(transformation(extent={{-86,-96},{-76,-86}})));
    equation
      connect(relAirMas.relAirMas, skyBri.relAirMas) annotation (Line(
          points={{-71.6,-40},{-66,-40},{-66,-48.4},{-60.8,-48.4}},
          color={0,0,127}));
      connect(skyBri.skyBri, briCoe.skyBri) annotation (Line(
          points={{-51.6,-50},{-46,-50},{-46,-30},{-40.8,-30}},
          color={0,0,127}));
      connect(skyCle.skyCle, briCoe.skyCle) annotation (Line(
          points={{-53.6,20},{-46,20},{-46,-27.6},{-40.8,-27.6}},
          color={0,0,127}));
      connect(incAng.y, HDifTil.incAng) annotation (Line(
          points={{-75.5,-91},{-16,-91},{-16,-16},{-4.2,-16},{-4.2,-14.7}},
          color={0,0,127}));
      connect(weaBus.solZen, skyCle.zen) annotation (Line(
          points={{-100,5.55112e-16},{-86,5.55112e-16},{-86,17.6},{-62.8,17.6}},
          color={0,0,127}));
      connect(weaBus.solZen, relAirMas.zen) annotation (Line(
          points={{-100,5.55112e-16},{-86,5.55112e-16},{-86,-40},{-80.8,-40}},
          color={0,0,127}));
      connect(weaBus.solZen, briCoe.zen) annotation (Line(
          points={{-100,5.55112e-16},{-86,5.55112e-16},{-86,-20},{-66,-20},{-66,-32},
              {-40.8,-32},{-40.8,-32.4}},
          color={0,0,127}));
      connect(weaBus.HGloHor, skyCle.HGloHor) annotation (Line(
          points={{-100,5.55112e-16},{-92,5.55112e-16},{-92,22.4},{-62.8,22.4}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.HDifHor, skyCle.HDifHor) annotation (Line(
          points={{-100,5.55112e-16},{-92,5.55112e-16},{-92,20},{-62.8,20}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.HDifHor, skyBri.HDifHor) annotation (Line(
          points={{-100,5.55112e-16},{-92,5.55112e-16},{-92,-51.6},{-60.8,-51.6}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.HGloHor, HDifTil.HGloHor) annotation (Line(
          points={{-100,5.55112e-16},{-70,0},{-38,0},{-38,16.8},{-4.2,16.8}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.HDifHor, HDifTil.HDifHor) annotation (Line(
          points={{-100,5.55112e-16},{-38,5.55112e-16},{-38,10},{-4.2,10},{-4.2,
              10.5}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(briCoe.F2, HDifTil.briCof2) annotation (Line(
          points={{-31.6,-31.6},{-24,-31.6},{-24,-2.1},{-4.2,-2.1}},
          color={0,0,127}));
      connect(briCoe.F1, HDifTil.briCof1) annotation (Line(
          points={{-31.6,-28.4},{-28,-28.4},{-28,4.2},{-4.2,4.2}},
          color={0,0,127}));
      connect(weaBus, incAng.weaBus) annotation (Line(
          points={{-100,5.55112e-016},{-92,5.55112e-016},{-92,-91},{-86,-91}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.solZen, HDifTil.zen) annotation (Line(
          points={{-100,5.55112e-16},{-86,5.55112e-16},{-86,-58},{-20,-58},{-20,
              -8.4},{-4.2,-8.4}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(HDifTil.HSkyDifTil, add.u1) annotation (Line(
          points={{44.1,8.4},{52,8.4},{52,6},{58,6}},
          color={0,0,127}));
      connect(HDifTil.HGroDifTil, add.u2) annotation (Line(
          points={{44.1,-8.4},{52,-8.4},{52,-6},{58,-6}},
          color={0,0,127}));
      connect(add.y, H) annotation (Line(
          points={{81,6.10623e-16},{90.5,6.10623e-16},{90.5,5.55112e-16},{110,
              5.55112e-16}},
          color={0,0,127}));
      connect(HDifTil.HSkyDifTil, HSkyDifTil) annotation (Line(
          points={{44.1,8.4},{52,8.4},{52,60},{110,60}},
          color={0,0,127}));
      connect(HDifTil.HGroDifTil, HGroDifTil) annotation (Line(
          points={{44.1,-8.4},{52,-8.4},{52,-60},{110,-60}},
          color={0,0,127}));
      annotation (
        defaultComponentName="HDifTil",
        Documentation(info="<html>
<p>
This component computes the hemispherical diffuse irradiation on a tilted surface using an anisotropic
sky model proposed by Perez.
For a definition of the parameters, see the
<a href=\"modelica://Buildings.BoundaryConditions.UsersGuide\">User's Guide</a>.
</p>
<h4>References</h4>
<ul>
<li>
P. Ineichen, R. Perez and R. Seals (1987).
<i>The Importance of Correct Albedo Determination for Adequately Modeling Energy Received by Tilted Surface</i>,
Solar Energy, 39(4): 301-305.
</li>
<li>
R. Perez, R. Seals, P. Ineichen, R. Stewart and D. Menicucci (1987).
<i>A New Simplified Version of the Perez Diffuse Irradiance Model for Tilted Surface</i>,
Solar Energy, 39(3): 221-231.
</li>
<li>
R. Perez, P. Ineichen, R. Seals, J. Michalsky and R. Stewart (1990).
<i>Modeling Dyalight Availability and Irradiance Componets From Direct and Global Irradiance</i>,
Solar Energy, 44(5):271-289.
</li>
</ul>
</html>",     revisions="<html>
<ul>
<li>
November 14, 2015, by Michael Wetter:<br/>
Added <code>min</code>, <code>max</code> and <code>unit</code>
attributes for <code>rho</code>.
</li>
<li>
June 6, 2012, by Wangda Zuo:<br/>
Added contributions from sky and ground that were separated in base class.
</li>
<li>
February 25, 2012, by Michael Wetter:<br/>
Changed component to get zenith angle from weather bus.
</li>
<li>
May 24, 2010, by Wangda Zuo:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(coordinateSystem(preserveAspectRatio=true, extent={{-100,-100},{100,
                100}}), graphics={Text(
              extent={{-150,110},{150,150}},
              textString="%name",
              lineColor={0,0,255})}));
    end DiffusePerez;

    block DirectTiltedSurface "Direct solar irradiation on a tilted surface"
      extends
        Buildings.BoundaryConditions.SolarIrradiation.BaseClasses.PartialSolarIrradiation;
      parameter Modelica.SIunits.Angle lat "Latitude";
      parameter Modelica.SIunits.Angle azi "Surface azimuth";
      Modelica.Blocks.Interfaces.RealOutput inc(
         quantity="Angle",
         unit="rad",
        displayUnit="deg") "Incidence angle"
        annotation (Placement(transformation(extent={{100,-50},{120,-30}})));
    protected
      IncidenceAngle incAng(
        azi=azi,
        til=til,
        lat=lat) "Incidence angle"
        annotation (Placement(transformation(extent={{-50,-30},{-30,-10}})));
      DirectTiltedSurface_sub HDirTil "Direct irradition on tilted surface"
        annotation (Placement(transformation(extent={{0,-20},{40,20}})));
    equation
      connect(incAng.y, HDirTil.incAng) annotation (Line(
          points={{-29,-20},{-12,-20},{-12,-12},{-4,-12}},
          color={0,0,127}));
      connect(weaBus.HDirNor, HDirTil.HDirNor) annotation (Line(
          points={{-100,5.55112e-16},{-80,5.55112e-16},{-80,12},{-4,12}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(incAng.y, inc) annotation (Line(
          points={{-29,-20},{-20,-20},{-20,-40},{110,-40}},
          color={0,0,127}));
      connect(HDirTil.HDirTil, H) annotation (Line(
          points={{42,1.22125e-15},{72,1.22125e-15},{72,5.55112e-16},{110,
              5.55112e-16}},
          color={0,0,127}));
      connect(weaBus, incAng.weaBus) annotation (Line(
          points={{-100,5.55112e-16},{-80,5.55112e-16},{-80,-20},{-50,-20}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      annotation (
        defaultComponentName="HDirTil",
        Documentation(info="<html>
<p>
This component computes the direct solar irradiation on a tilted surface.
For a definition of the parameters, see the
<a href=\"modelica://Buildings.BoundaryConditions.UsersGuide\">User's Guide</a>.
</p>
</html>",     revisions="<html>
<ul>
<li>
April 21, 2016, by Michael Wetter:<br/>
Removed duplicate instance <code>weaBus</code>.
This is for
<a href=\"https://github.com/ibpsa/modelica/issues/461\">
https://github.com/ibpsa/modelica/issues/461</a>.
</li>
<li>
December 12, 2010, by Michael Wetter:<br/>
Added incidence angle as output as this is needed for the room model.
</li>
<li>
May 24, 2010, by Wangda Zuo:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(coordinateSystem(preserveAspectRatio=true, extent={{-100,-100},{100,
                100}}), graphics={Text(
              extent={{-150,110},{150,150}},
              textString="%name",
              lineColor={0,0,255})}));
    end DirectTiltedSurface;

    block IncidenceAngle "Solar incidence angle on a tilted surface"
      extends Modelica.Blocks.Icons.Block;
      parameter Modelica.SIunits.Angle lat "Latitude";
      parameter Modelica.SIunits.Angle azi "Surface azimuth";
      parameter Modelica.SIunits.Angle til "Surface tilt";
      Modelica.Blocks.Interfaces.RealOutput y(
        quantity="Angle",
        unit="rad",
        displayUnit="deg") "Incidence angle" annotation (Placement(transformation(
              extent={{100,-10},{120,10}}), iconTransformation(extent={{100,-10},{
                120,10}})));
      Buildings.BoundaryConditions.WeatherData.Bus weaBus "Weather data"
        annotation (Placement(transformation(extent={{-110,-10},{-90,10}})));
    protected
      Buildings.BoundaryConditions.SolarGeometry.BaseClasses.Declination decAng
        "Declination angle"
        annotation (Placement(transformation(extent={{-40,30},{-20,50}})));
      Buildings.BoundaryConditions.SolarGeometry.BaseClasses.SolarHourAngle
        solHouAng "Solar hour angle"
        annotation (Placement(transformation(extent={{-40,-50},{-20,-30}})));
      Buildings.BoundaryConditions.SolarGeometry.BaseClasses.IncidenceAngle incAng(
        lat=lat,
        azi=azi,
        til=til) "Incidence angle"
        annotation (Placement(transformation(extent={{40,-10},{60,10}})));
    equation
      connect(incAng.incAng, y) annotation (Line(
          points={{61,0},{88.25,0},{88.25,1.16573e-015},{95.5,1.16573e-015},{95.5,0},
              {110,0}},
          color={0,0,127}));
      connect(decAng.decAng, incAng.decAng) annotation (Line(
          points={{-19,40},{20,40},{20,5.4},{37.8,5.4}},
          color={0,0,127}));
      connect(solHouAng.solHouAng, incAng.solHouAng) annotation (Line(
          points={{-19,-40},{20,-40},{20,-4.8},{38,-4.8}},
          color={0,0,127}));
      connect(weaBus.cloTim, decAng.nDay) annotation (Line(
          points={{-100,0},{-80,0},{-80,40},{-42,40}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      connect(weaBus.solTim, solHouAng.solTim) annotation (Line(
          points={{-100,0},{-80,0},{-80,-40},{-42,-40}},
          color={255,204,51},
          thickness=0.5), Text(
          string="%first",
          index=-1,
          extent={{-6,3},{-6,3}}));
      annotation (
        defaultComponentName="incAng",
        Documentation(info="<html>
<p>
This component computes the solar incidence angle on a tilted surface.
For a definition of the parameters, see the User's Guide
<a href=\"modelica://Buildings.BoundaryConditions.UsersGuide\">Buildings.BoundaryConditions.UsersGuide</a>.
</p>
</html>",     revisions="<html>
<ul>
<li>
November 30, 2011, by Michael Wetter:<br/>
Removed <code>connect(y, y)</code> statement.
</li>
<li>
February 28, 2011, by Wangda Zuo:<br/>
Use local civil time instead of clock time.
</li>
<li>
May 19, 2010, by Wangda Zuo:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(coordinateSystem(preserveAspectRatio=true, extent={{-100,-100},{100,
                100}}), graphics={Text(
              extent={{-150,110},{150,150}},
              textString="%name",
              lineColor={0,0,255}), Bitmap(extent={{-90,90},{90,-92}}, fileName=
                  "modelica://Buildings/Resources/Images/BoundaryConditions/SolarGeometry/BaseClasses/IncidenceAngle.png")}));
    end IncidenceAngle;

    block DirectTiltedSurface_sub
      "Direct solar irradiation on a tilted surface"
      extends Modelica.Blocks.Icons.Block;
      Modelica.Blocks.Interfaces.RealInput incAng(
        quantity="Angle",
        unit="rad",
        displayUnit="degree") "Incidence angle of the sun beam on a tilted surface"
        annotation (Placement(transformation(extent={{-140,-80},{-100,-40}})));
      Modelica.Blocks.Interfaces.RealInput HDirNor(quantity=
            "RadiantEnergyFluenceRate", unit="W/m2") "Direct normal radiation"
        annotation (Placement(transformation(extent={{-140,40},{-100,80}})));
      Modelica.Blocks.Interfaces.RealOutput HDirTil(quantity=
            "RadiantEnergyFluenceRate", unit="W/m2")
        "Direct solar irradiation on a tilted surface"
        annotation (Placement(transformation(extent={{100,-10},{120,10}})));
    equation
      HDirTil =  max(0, Modelica.Math.cos(incAng)*HDirNor);
      annotation (
        defaultComponentName="HDirTil",
        Documentation(info="<html>
<p>
This component computes the direct solar irradiation on a tilted surface.
</p>
</html>",     revisions="<html>
<ul>
<li>
May 5, 2015, by Filip Jorissen:<br/>
Converted <code>algorithm</code> section into
<code>equation</code> section for easier differentiability.
</li>
<li>
May 24, 2010, by Wangda Zuo:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(coordinateSystem(preserveAspectRatio=true, extent={{-100,-100},{100,
                100}}), graphics={
            Text(
              extent={{-150,110},{150,150}},
              textString="%name",
              lineColor={0,0,255}),
            Text(
              extent={{-50,56},{-102,68}},
              lineColor={0,0,127},
              textString="HDirNor"),
            Text(
              extent={{-54,-66},{-106,-54}},
              lineColor={0,0,127},
              textString="incAng")}));
    end DirectTiltedSurface_sub;

    block DiffusePerez_sub
      "Hemispherical diffuse irradiation on a tilted surface with Perez's anisotropic model"
      extends Modelica.Blocks.Icons.Block;
      parameter Real rho=0.2 "Ground reflectance";
      parameter Modelica.SIunits.Angle til(displayUnit="deg") "Surface tilt angle";
      Modelica.Blocks.Interfaces.RealInput briCof1 "Brightening Coeffcient F1"
        annotation (Placement(transformation(extent={{-140,0},{-100,40}})));
      Modelica.Blocks.Interfaces.RealInput briCof2 "Brightening Coeffcient F2"
        annotation (Placement(transformation(extent={{-140,-30},{-100,10}})));
      Modelica.Blocks.Interfaces.RealInput HDifHor(quantity=
            "RadiantEnergyFluenceRate", unit="W/m2")
        "Diffuse horizontal solar radiation"
        annotation (Placement(transformation(extent={{-140,30},{-100,70}})));
      Modelica.Blocks.Interfaces.RealInput HGloHor(quantity=
            "RadiantEnergyFluenceRate", unit="W/m2")
        "Global horizontal radiation"
        annotation (Placement(transformation(extent={{-140,60},{-100,100}})));
      Modelica.Blocks.Interfaces.RealInput zen(
        quantity="Angle",
        unit="rad",
        displayUnit="degree") "Zenith angle of the sun beam"
        annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
      Modelica.Blocks.Interfaces.RealInput incAng(
        quantity="Angle",
        unit="rad",
        displayUnit="degree") "Solar incidence angle on the surface"
        annotation (Placement(transformation(extent={{-140,-90},{-100,-50}})));
      Modelica.Blocks.Interfaces.RealOutput HGroDifTil(final quantity=
            "RadiantEnergyFluenceRate", final unit="W/m2")
        "Hemispherical diffuse solar irradiation on a tilted surface from the ground"
        annotation (Placement(transformation(extent={{100,-50},{120,-30}})));
      Modelica.Blocks.Interfaces.RealOutput HSkyDifTil(final quantity=
            "RadiantEnergyFluenceRate", final unit="W/m2")
        "Hemispherical diffuse solar irradiation on a tilted surface from the sky"
        annotation (Placement(transformation(extent={{100,30},{120,50}})));
    protected
      Real a;
      Real b;
      constant Real bMin=Modelica.Math.cos(Modelica.Constants.pi*85/180)
        "Lower bound for b";
    equation
      a = Buildings.Utilities.Math.Functions.smoothMax(
        0,
        Modelica.Math.cos(incAng),
        0.01);
      b = Buildings.Utilities.Math.Functions.smoothMax(
        bMin,
        Modelica.Math.cos(zen),
        0.01);
      HSkyDifTil = HDifHor*(0.5*(1 - briCof1)*(1 + Modelica.Math.cos(til)) +
        briCof1*a/b + briCof2*Modelica.Math.sin(til));
      HGroDifTil = HGloHor*0.5*rho*(1 - Modelica.Math.cos(til));
      annotation (
        defaultComponentName="HDifTil",
        Documentation(info="<html>
<p>
This component computes the hemispherical diffuse irradiation on a tilted surface by using an anisotropic model proposed by Perez.
</p>
<h4>References</h4>
<ul>
<li>
P. Ineichen, R. Perez and R. Seals (1987).
<i>The Importance of Correct Albedo Determination for Adequately Modeling Energy Received by Tilted Surface</i>,
Solar Energy, 39(4): 301-305.
</li>
<li>
R. Perez, R. Seals, P. Ineichen, R. Stewart and D. Menicucci (1987).
<i>A New Simplified Version of the Perez Diffuse Irradiance Model for Tilted Surface</i>,
Solar Energy, 39(3): 221-231.
</li>
<li>
R. Perez, P. Ineichen, R. Seals, J. Michalsky and R. Stewart (1990).
<i>Modeling Dyalight Availability and Irradiance Componets From Direct and Global Irradiance</i>,
Solar Energy, 44(5):271-289.
</li>
</ul>
</html>",     revisions="<html>
<ul>
<li>
June 6, 2012, by Wangda Zuo:<br/>
Separated the contribution from the sky and the ground.
</li>
</ul>
<ul>
<li>
May 24, 2010, by Wangda Zuo:<br/>
First implementation.
</li>
</ul>
</html>"),
        Icon(coordinateSystem(preserveAspectRatio=true, extent={{-100,-100},{100,
                100}}), graphics={
            Text(
              extent={{-150,110},{150,150}},
              textString="%name",
              lineColor={0,0,255}),
            Text(
              extent={{-48,74},{-100,86}},
              lineColor={0,0,127},
              textString="HGloHor"),
            Text(
              extent={{-50,44},{-102,56}},
              lineColor={0,0,127},
              textString="HDifHor"),
            Text(
              extent={{-50,14},{-102,26}},
              lineColor={0,0,127},
              textString="briCof1"),
            Text(
              extent={{-50,-16},{-102,-4}},
              lineColor={0,0,127},
              textString="briCof2"),
            Text(
              extent={{-50,-46},{-102,-34}},
              lineColor={0,0,127},
              textString="zen"),
            Text(
              extent={{-52,-76},{-104,-64}},
              lineColor={0,0,127},
              textString="incAng")}));
    end DiffusePerez_sub;

    package Examples
    end Examples;
  end Solar;

  package InverterModel
    package Models
      model Inverter_simple
        parameter Real fixed_mode=0 "Inverter mode (0-Fixed P; 1-Fixed S)";
        Modelica.Blocks.Interfaces.RealInput PV_generation "PV generation [W]"
          annotation (Placement(transformation(extent={{-140,20},{-100,60}})));
        Modelica.Blocks.Interfaces.RealOutput ActivePower "Output of active power [W]"
          annotation (Placement(transformation(extent={{100,50},{120,70}})));
        Modelica.Blocks.Interfaces.RealOutput ReactivePower "Output of reactive power [Var]"
          annotation (Placement(transformation(extent={{100,-70},{120,-50}})));
        Modelica.Blocks.Interfaces.RealInput pf "Input of power factor"
          annotation (Placement(transformation(extent={{-140,-60},{-100,-20}})));
        Modelica.Blocks.Interfaces.RealOutput ApparentPower "Output of apparent  power [VA]"
          annotation (Placement(transformation(extent={{100,-10},{120,10}})));
      equation
        if fixed_mode == 0 then // fixed P
          ActivePower = PV_generation;
          ApparentPower = PV_generation / pf;
          ReactivePower = sqrt(ApparentPower^2 - ActivePower^2);
        elseif fixed_mode == 1 then // fixed S
          ApparentPower = PV_generation;
          ActivePower = ApparentPower * pf;
          ReactivePower = sqrt(ApparentPower^2 - ActivePower^2);
        end if
          annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Inverter_simple;
    end Models;

    package Examples
      model Test_Inverter_simple
        Models.Inverter_simple P_fixed(fixed_mode=0)
          annotation (Placement(transformation(extent={{-10,20},{10,40}})));
        Models.Inverter_simple S_fixed(fixed_mode=1)
          annotation (Placement(transformation(extent={{-10,-40},{10,-20}})));
        Modelica.Blocks.Sources.Constant PV_generation(k=100)
          annotation (Placement(transformation(extent={{-100,60},{-80,80}})));
        Modelica.Blocks.Sources.Ramp Power_factor(
          duration=1,
          height=0.9,
          offset=0.1)
          annotation (Placement(transformation(extent={{-100,16},{-80,36}})));
      equation
        connect(PV_generation.y, P_fixed.PV_generatoin) annotation (Line(points=
               {{-79,70},{-30,70},{-30,34},{-12,34}}, color={0,0,127}));
        connect(S_fixed.PV_generatoin, PV_generation.y) annotation (Line(points=
               {{-12,-26},{-30,-26},{-30,70},{-79,70}}, color={0,0,127}));
        connect(Power_factor.y, P_fixed.pf)
          annotation (Line(points={{-79,26},{-12,26}}, color={0,0,127}));
        connect(Power_factor.y, S_fixed.pf) annotation (Line(points={{-79,26},{
                -50,26},{-50,-34},{-12,-34}}, color={0,0,127}));
        annotation (Icon(coordinateSystem(preserveAspectRatio=false)), Diagram(
              coordinateSystem(preserveAspectRatio=false)));
      end Test_Inverter_simple;
    end Examples;
  end InverterModel;
  annotation (uses(Modelica(version="3.2.2"),
      Flexgrid(version="3"),
      Buildings(version="5.0.2")),
    version="1",
    conversion(noneFromVersion=""));
end CyDER;
