/*
 * compilation_1_sm_computation_data.c
 *
 * Code generation for model "compilation_1_sm_computation.mdl".
 *
 * Model version              : 1.105
 * Simulink Coder version : 8.1 (R2011b) 08-Jul-2011
 * C source code generated on : Thu Aug 24 16:36:55 2017
 *
 * Target selection: rtlab_rtmodel.tlc
 * Note: GRT includes extra infrastructure and instrumentation for prototyping
 * Embedded hardware selection: 32-bit Generic
 * Code generation objectives: Unspecified
 * Validation result: Not run
 */
#include "compilation_1_sm_computation.h"
#include "compilation_1_sm_computation_private.h"

/* Block parameters (auto storage) */
Parameters_compilation_1_sm_computation compilation_1_sm_computation_P = {
  0.0,                                 /* Expression: 0
                                        * Referenced by: '<S1>/S-Function1'
                                        */
  0.0,                                 /* Expression: 0
                                        * Referenced by: '<S1>/S-Function'
                                        */

  /*  Computed Parameter: SFunction_P1_Size
   * Referenced by: '<S5>/S-Function'
   */
  { 1.0, 1.0 },
  1.0,                                 /* Expression: Data_width
                                        * Referenced by: '<S5>/S-Function'
                                        */

  /*  Computed Parameter: SFunction_P2_Size
   * Referenced by: '<S5>/S-Function'
   */
  { 1.0, 1.0 },
  93.5,                                /* Expression: InitialConditions
                                        * Referenced by: '<S5>/S-Function'
                                        */
  0.0,                                 /* Expression: 0
                                        * Referenced by: '<S2>/Integrator3'
                                        */
  200.0,                               /* Expression: 200
                                        * Referenced by: '<S2>/Integrator3'
                                        */
  0.0,                                 /* Expression: 0
                                        * Referenced by: '<S2>/Integrator3'
                                        */
  0.005,                               /* Expression: 0.005
                                        * Referenced by: '<S2>/Sensor response time'
                                        */
  0.0,                                 /* Expression: 0
                                        * Referenced by: '<S2>/Sensor response time'
                                        */
  20.0,                                /* Expression: 20
                                        * Referenced by: '<S2>/Gain Kp'
                                        */
  0.0,                                 /* Expression: 0
                                        * Referenced by: '<S2>/Integrator1'
                                        */
  5.0,                                 /* Expression: 5
                                        * Referenced by: '<S2>/Gain Ki'
                                        */
  -1.0,                                /* Expression: -1
                                        * Referenced by: '<S2>/Gain1'
                                        */
  5.0,                                 /* Expression: 5
                                        * Referenced by: '<S2>/Gain Kd'
                                        */

  /*  Computed Parameter: SFunction_P1_Size_d
   * Referenced by: '<S9>/S-Function'
   */
  { 1.0, 1.0 },
  1.0,                                 /* Expression: Acqu_group
                                        * Referenced by: '<S9>/S-Function'
                                        */
  0.005,                               /* Expression: 0.005
                                        * Referenced by: '<S2>/Actuator response time'
                                        */
  0.0,                                 /* Expression: 0
                                        * Referenced by: '<S2>/Actuator response time'
                                        */
  1.0,                                 /* Expression: 1
                                        * Referenced by: '<S2>/Gain'
                                        */
  0.0                                  /* Expression: 0
                                        * Referenced by: '<S2>/Integrator2'
                                        */
};
