/*
 * compilation_1_sm_computation.c
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

/* Block signals (auto storage) */
BlockIO_compilation_1_sm_computation compilation_1_sm_computation_B;

/* Continuous states */
ContinuousStates_compilation_1_sm_computation compilation_1_sm_computation_X;

/* Block states (auto storage) */
D_Work_compilation_1_sm_computation compilation_1_sm_computation_DWork;

/* Real-time model */
RT_MODEL_compilation_1_sm_computation compilation_1_sm_computation_M_;
RT_MODEL_compilation_1_sm_computation *const compilation_1_sm_computation_M =
  &compilation_1_sm_computation_M_;

/*
 * Time delay interpolation routine
 *
 * The linear interpolation is performed using the formula:
 *
 *          (t2 - tMinusDelay)         (tMinusDelay - t1)
 * u(t)  =  ----------------- * u1  +  ------------------- * u2
 *              (t2 - t1)                  (t2 - t1)
 */
real_T rt_TDelayInterpolate(
  real_T tMinusDelay,                  /* tMinusDelay = currentSimTime - delay */
  real_T tStart,
  real_T *tBuf,
  real_T *uBuf,
  int_T bufSz,
  int_T *lastIdx,
  int_T oldestIdx,
  int_T newIdx,
  real_T initOutput,
  boolean_T discrete,
  boolean_T minorStepAndTAtLastMajorOutput)
{
  int_T i;
  real_T yout, t1, t2, u1, u2;

  /*
   * If tMinusDelay is less than zero, should output initial value
   */
  if (tMinusDelay <= tStart)
    return initOutput;

  /* For fixed buffer extrapolation:
   * if tMinusDelay is small than the time at oldestIdx, if discrete, output
   * tailptr value,  else use tailptr and tailptr+1 value to extrapolate
   * It is also for fixed buffer. Note: The same condition can happen for transport delay block where
   * use tStart and and t[tail] other than using t[tail] and t[tail+1].
   * See below
   */
  if ((tMinusDelay <= tBuf[oldestIdx] ) ) {
    if (discrete) {
      return(uBuf[oldestIdx]);
    } else {
      int_T tempIdx= oldestIdx + 1;
      if (oldestIdx == bufSz-1)
        tempIdx = 0;
      t1= tBuf[oldestIdx];
      t2= tBuf[tempIdx];
      u1= uBuf[oldestIdx];
      u2= uBuf[tempIdx];
      if (t2 == t1) {
        if (tMinusDelay >= t2) {
          yout = u2;
        } else {
          yout = u1;
        }
      } else {
        real_T f1 = (t2-tMinusDelay) / (t2-t1);
        real_T f2 = 1.0 - f1;

        /*
         * Use Lagrange's interpolation formula.  Exact outputs at t1, t2.
         */
        yout = f1*u1 + f2*u2;
      }

      return yout;
    }
  }

  /*
   * When block does not have direct feedthrough, we use the table of
   * values to extrapolate off the end of the table for delays that are less
   * than 0 (less then step size).  This is not completely accurate.  The
   * chain of events is as follows for a given time t.  Major output - look
   * in table.  Update - add entry to table.  Now, if we call the output at
   * time t again, there is a new entry in the table. For very small delays,
   * this means that we will have a different answer from the previous call
   * to the output fcn at the same time t.  The following code prevents this
   * from happening.
   */
  if (minorStepAndTAtLastMajorOutput) {
    /* pretend that the new entry has not been added to table */
    if (newIdx != 0) {
      if (*lastIdx == newIdx) {
        (*lastIdx)--;
      }

      newIdx--;
    } else {
      if (*lastIdx == newIdx) {
        *lastIdx = bufSz-1;
      }

      newIdx = bufSz - 1;
    }
  }

  i = *lastIdx;
  if (tBuf[i] < tMinusDelay) {
    /* Look forward starting at last index */
    while (tBuf[i] < tMinusDelay) {
      /* May occur if the delay is less than step-size - extrapolate */
      if (i == newIdx)
        break;
      i = ( i < (bufSz-1) ) ? (i+1) : 0;/* move through buffer */
    }
  } else {
    /*
     * Look backwards starting at last index which can happen when the
     * delay time increases.
     */
    while (tBuf[i] >= tMinusDelay) {
      /*
       * Due to the entry condition at top of function, we
       * should never hit the end.
       */
      i = (i > 0) ? i-1 : (bufSz-1);   /* move through buffer */
    }

    i = ( i < (bufSz-1) ) ? (i+1) : 0;
  }

  *lastIdx = i;
  if (discrete) {
    /*
     * tempEps = 128 * eps;
     * localEps = max(tempEps, tempEps*fabs(tBuf[i]))/2;
     */
    double tempEps = (DBL_EPSILON) * 128.0;
    double localEps = tempEps * fabs(tBuf[i]);
    if (tempEps > localEps) {
      localEps = tempEps;
    }

    localEps = localEps / 2.0;
    if (tMinusDelay >= (tBuf[i] - localEps)) {
      yout = uBuf[i];
    } else {
      if (i == 0) {
        yout = uBuf[bufSz-1];
      } else {
        yout = uBuf[i-1];
      }
    }
  } else {
    if (i == 0) {
      t1 = tBuf[bufSz-1];
      u1 = uBuf[bufSz-1];
    } else {
      t1 = tBuf[i-1];
      u1 = uBuf[i-1];
    }

    t2 = tBuf[i];
    u2 = uBuf[i];
    if (t2 == t1) {
      if (tMinusDelay >= t2) {
        yout = u2;
      } else {
        yout = u1;
      }
    } else {
      real_T f1 = (t2-tMinusDelay) / (t2-t1);
      real_T f2 = 1.0 - f1;

      /*
       * Use Lagrange's interpolation formula.  Exact outputs at t1, t2.
       */
      yout = f1*u1 + f2*u2;
    }
  }

  return(yout);
}

/*
 * This function updates continuous states using the ODE4 fixed-step
 * solver algorithm
 */
static void rt_ertODEUpdateContinuousStates(RTWSolverInfo *si )
{
  time_T t = rtsiGetT(si);
  time_T tnew = rtsiGetSolverStopTime(si);
  time_T h = rtsiGetStepSize(si);
  real_T *x = rtsiGetContStates(si);
  ODE4_IntgData *id = (ODE4_IntgData *)rtsiGetSolverData(si);
  real_T *y = id->y;
  real_T *f0 = id->f[0];
  real_T *f1 = id->f[1];
  real_T *f2 = id->f[2];
  real_T *f3 = id->f[3];
  real_T temp;
  int_T i;
  int_T nXc = 3;
  rtsiSetSimTimeStep(si,MINOR_TIME_STEP);

  /* Save the state values at time t in y, we'll use x as ynew. */
  (void) memcpy(y, x,
                nXc*sizeof(real_T));

  /* Assumes that rtsiSetT and ModelOutputs are up-to-date */
  /* f0 = f(t,y) */
  rtsiSetdX(si, f0);
  compilation_1_sm_computation_derivatives();

  /* f1 = f(t + (h/2), y + (h/2)*f0) */
  temp = 0.5 * h;
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (temp*f0[i]);
  }

  rtsiSetT(si, t + temp);
  rtsiSetdX(si, f1);
  compilation_1_sm_computation_output(0);
  compilation_1_sm_computation_derivatives();

  /* f2 = f(t + (h/2), y + (h/2)*f1) */
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (temp*f1[i]);
  }

  rtsiSetdX(si, f2);
  compilation_1_sm_computation_output(0);
  compilation_1_sm_computation_derivatives();

  /* f3 = f(t + h, y + h*f2) */
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + (h*f2[i]);
  }

  rtsiSetT(si, tnew);
  rtsiSetdX(si, f3);
  compilation_1_sm_computation_output(0);
  compilation_1_sm_computation_derivatives();

  /* tnew = t + h
     ynew = y + (h/6)*(f0 + 2*f1 + 2*f2 + 2*f3) */
  temp = h / 6.0;
  for (i = 0; i < nXc; i++) {
    x[i] = y[i] + temp*(f0[i] + 2.0*f1[i] + 2.0*f2[i] + f3[i]);
  }

  rtsiSetSimTimeStep(si,MAJOR_TIME_STEP);
}

/* Model output function */
void compilation_1_sm_computation_output(int_T tid)
{
  /* local block i/o variables */
  real_T rtb_Sensorresponsetime;
  real_T rtb_Actuatorresponsetime;
  real_T rtb_test5;
  real_T rtb_test4;
  if (rtmIsMajorTimeStep(compilation_1_sm_computation_M)) {
    /* set solver stop time */
    if (!(compilation_1_sm_computation_M->Timing.clockTick0+1)) {
      rtsiSetSolverStopTime(&compilation_1_sm_computation_M->solverInfo,
                            ((compilation_1_sm_computation_M->Timing.clockTickH0
        + 1) * compilation_1_sm_computation_M->Timing.stepSize0 * 4294967296.0));
    } else {
      rtsiSetSolverStopTime(&compilation_1_sm_computation_M->solverInfo,
                            ((compilation_1_sm_computation_M->Timing.clockTick0
        + 1) * compilation_1_sm_computation_M->Timing.stepSize0 +
        compilation_1_sm_computation_M->Timing.clockTickH0 *
        compilation_1_sm_computation_M->Timing.stepSize0 * 4294967296.0));
    }
  }                                    /* end MajorTimeStep */

  /* Update absolute time of base rate at minor time step */
  if (rtmIsMinorTimeStep(compilation_1_sm_computation_M)) {
    compilation_1_sm_computation_M->Timing.t[0] = rtsiGetT
      (&compilation_1_sm_computation_M->solverInfo);
  }

  if (rtmIsMajorTimeStep(compilation_1_sm_computation_M)) {
    /* Sum: '<S1>/Sum' incorporates:
     *  Constant: '<S1>/S-Function1'
     *  Memory: '<S1>/S-Function'
     */
    compilation_1_sm_computation_B.Sum =
      compilation_1_sm_computation_P.SFunction1_Value +
      compilation_1_sm_computation_DWork.SFunction_PreviousInput;

    /* Stop: '<S1>/Stop Simulation' */
    if (compilation_1_sm_computation_B.Sum != 0.0) {
      rtmSetStopRequested(compilation_1_sm_computation_M, 1);
    }

    /* End of Stop: '<S1>/Stop Simulation' */

    /* Level2 S-Function Block: '<S5>/S-Function' (RECV_Param) */
    {
      SimStruct *rts = compilation_1_sm_computation_M->childSfunctions[0];
      sfcnOutputs(rts, 1);
    }
  }

  /* Integrator: '<S2>/Integrator3'
   *
   * Regarding '<S2>/Integrator3':
   *  Limited Integrator
   */
  if (compilation_1_sm_computation_X.Integrator3_CSTATE >=
      compilation_1_sm_computation_P.Integrator3_UpperSat ) {
    compilation_1_sm_computation_X.Integrator3_CSTATE =
      compilation_1_sm_computation_P.Integrator3_UpperSat;
  } else if (compilation_1_sm_computation_X.Integrator3_CSTATE <=
             compilation_1_sm_computation_P.Integrator3_LowerSat ) {
    compilation_1_sm_computation_X.Integrator3_CSTATE =
      compilation_1_sm_computation_P.Integrator3_LowerSat;
  }

  compilation_1_sm_computation_B.d =
    compilation_1_sm_computation_X.Integrator3_CSTATE;

  /* TransportDelay: '<S2>/Sensor response time' */
  {
    real_T **uBuffer = (real_T**)
      &compilation_1_sm_computation_DWork.Sensorresponsetime_PWORK.TUbufferPtrs
      [0];
    real_T **tBuffer = (real_T**)
      &compilation_1_sm_computation_DWork.Sensorresponsetime_PWORK.TUbufferPtrs
      [1];
    real_T simTime = compilation_1_sm_computation_M->Timing.t[0];
    real_T tMinusDelay = simTime -
      compilation_1_sm_computation_P.Sensorresponsetime_Delay;
    rtb_Sensorresponsetime = rt_TDelayInterpolate(
      tMinusDelay,
      0.0,
      *tBuffer,
      *uBuffer,
      compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.CircularBufSize,
      &compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Last,
      compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Tail,
      compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Head,
      compilation_1_sm_computation_P.Sensorresponsetime_InitOutput,
      0,
      0);
  }

  /* Sum: '<S2>/Sum3' */
  compilation_1_sm_computation_B.Error =
    compilation_1_sm_computation_B.SFunction - rtb_Sensorresponsetime;

  /* Gain: '<S2>/Gain Kp' */
  rtb_test5 = compilation_1_sm_computation_P.GainKp_Gain *
    compilation_1_sm_computation_B.Error;

  /* Integrator: '<S2>/Integrator1' */
  rtb_Actuatorresponsetime = compilation_1_sm_computation_X.Integrator1_CSTATE;

  /* Gain: '<S2>/Gain Ki' */
  rtb_test4 = compilation_1_sm_computation_P.GainKi_Gain *
    rtb_Actuatorresponsetime;

  /* Gain: '<S2>/Gain1' */
  compilation_1_sm_computation_B.Gain1 =
    compilation_1_sm_computation_P.Gain1_Gain * rtb_Sensorresponsetime;

  /* Derivative: '<S2>/Derivative1' */
  {
    real_T t = compilation_1_sm_computation_M->Timing.t[0];
    real_T timeStampA =
      compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampA;
    real_T timeStampB =
      compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampB;
    real_T *lastU =
      &compilation_1_sm_computation_DWork.Derivative1_RWORK.LastUAtTimeA;
    if (timeStampA >= t && timeStampB >= t) {
      rtb_Actuatorresponsetime = 0.0;
    } else {
      real_T deltaT;
      real_T lastTime = timeStampA;
      if (timeStampA < timeStampB) {
        if (timeStampB < t) {
          lastTime = timeStampB;
          lastU =
            &compilation_1_sm_computation_DWork.Derivative1_RWORK.LastUAtTimeB;
        }
      } else if (timeStampA >= t) {
        lastTime = timeStampB;
        lastU =
          &compilation_1_sm_computation_DWork.Derivative1_RWORK.LastUAtTimeB;
      }

      deltaT = t - lastTime;
      rtb_Actuatorresponsetime = (compilation_1_sm_computation_B.Gain1 - *lastU
        ++) / deltaT;
    }
  }

  /* Sum: '<S2>/Sum1' incorporates:
   *  Gain: '<S2>/Gain Kd'
   */
  compilation_1_sm_computation_B.c = (rtb_test5 + rtb_test4) +
    compilation_1_sm_computation_P.GainKd_Gain * rtb_Actuatorresponsetime;

  /* Clock: '<S2>/Clock' */
  compilation_1_sm_computation_B.e = compilation_1_sm_computation_M->Timing.t[0];
  if (rtmIsMajorTimeStep(compilation_1_sm_computation_M)) {
    /* Level2 S-Function Block: '<S9>/S-Function' (OP_SEND) */
    {
      SimStruct *rts = compilation_1_sm_computation_M->childSfunctions[1];
      sfcnOutputs(rts, 1);
    }
  }

  /* TransportDelay: '<S2>/Actuator response time' */
  {
    real_T **uBuffer = (real_T**)
      &compilation_1_sm_computation_DWork.Actuatorresponsetime_PWORK.TUbufferPtrs
      [0];
    real_T **tBuffer = (real_T**)
      &compilation_1_sm_computation_DWork.Actuatorresponsetime_PWORK.TUbufferPtrs
      [1];
    real_T simTime = compilation_1_sm_computation_M->Timing.t[0];
    real_T tMinusDelay = simTime -
      compilation_1_sm_computation_P.Actuatorresponsetime_Delay;
    rtb_Actuatorresponsetime = rt_TDelayInterpolate(
      tMinusDelay,
      0.0,
      *tBuffer,
      *uBuffer,
      compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.CircularBufSize,
      &compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Last,
      compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Tail,
      compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Head,
      compilation_1_sm_computation_P.Actuatorresponsetime_InitOutput,
      0,
      0);
  }

  /* Gain: '<S2>/Gain' */
  compilation_1_sm_computation_B.Gain = compilation_1_sm_computation_P.Gain_Gain
    * rtb_Actuatorresponsetime;

  /* Integrator: '<S2>/Integrator2' */
  compilation_1_sm_computation_B.plantresponse =
    compilation_1_sm_computation_X.Integrator2_CSTATE;

  /* tid is required for a uniform function interface.
   * Argument tid is not used in the function. */
  UNUSED_PARAMETER(tid);
}

/* Model update function */
void compilation_1_sm_computation_update(int_T tid)
{
  if (rtmIsMajorTimeStep(compilation_1_sm_computation_M)) {
    /* Update for Memory: '<S1>/S-Function' */
    compilation_1_sm_computation_DWork.SFunction_PreviousInput =
      compilation_1_sm_computation_B.Sum;
  }

  /* Update for TransportDelay: '<S2>/Sensor response time' */
  {
    real_T **uBuffer = (real_T**)
      &compilation_1_sm_computation_DWork.Sensorresponsetime_PWORK.TUbufferPtrs
      [0];
    real_T **tBuffer = (real_T**)
      &compilation_1_sm_computation_DWork.Sensorresponsetime_PWORK.TUbufferPtrs
      [1];
    real_T simTime = compilation_1_sm_computation_M->Timing.t[0];
    compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Head =
      ((compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Head <
        (compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.CircularBufSize
         -1)) ?
       (compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Head+1) : 0);
    if (compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Head ==
        compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Tail) {
      compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Tail =
        ((compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Tail <
          (compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.CircularBufSize
           -1)) ?
         (compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Tail+1) :
         0);
    }

    (*tBuffer)[compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Head]
      = simTime;
    (*uBuffer)[compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Head]
      = compilation_1_sm_computation_B.d;
  }

  /* Update for Derivative: '<S2>/Derivative1' */
  {
    real_T timeStampA =
      compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampA;
    real_T timeStampB =
      compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampB;
    real_T* lastTime =
      &compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampA;
    real_T* lastU =
      &compilation_1_sm_computation_DWork.Derivative1_RWORK.LastUAtTimeA;
    if (timeStampA != rtInf) {
      if (timeStampB == rtInf) {
        lastTime =
          &compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampB;
        lastU =
          &compilation_1_sm_computation_DWork.Derivative1_RWORK.LastUAtTimeB;
      } else if (timeStampA >= timeStampB) {
        lastTime =
          &compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampB;
        lastU =
          &compilation_1_sm_computation_DWork.Derivative1_RWORK.LastUAtTimeB;
      }
    }

    *lastTime = compilation_1_sm_computation_M->Timing.t[0];
    *lastU++ = compilation_1_sm_computation_B.Gain1;
  }

  /* Update for TransportDelay: '<S2>/Actuator response time' */
  {
    real_T **uBuffer = (real_T**)
      &compilation_1_sm_computation_DWork.Actuatorresponsetime_PWORK.TUbufferPtrs
      [0];
    real_T **tBuffer = (real_T**)
      &compilation_1_sm_computation_DWork.Actuatorresponsetime_PWORK.TUbufferPtrs
      [1];
    real_T simTime = compilation_1_sm_computation_M->Timing.t[0];
    compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Head =
      ((compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Head <
        (compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.CircularBufSize
         -1)) ?
       (compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Head+1) :
       0);
    if (compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Head ==
        compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Tail) {
      compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Tail =
        ((compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Tail <
          (compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.CircularBufSize
           -1)) ?
         (compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Tail+1) :
         0);
    }

    (*tBuffer)
      [compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Head] =
      simTime;
    (*uBuffer)
      [compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Head] =
      compilation_1_sm_computation_B.c;
  }

  if (rtmIsMajorTimeStep(compilation_1_sm_computation_M)) {
    rt_ertODEUpdateContinuousStates(&compilation_1_sm_computation_M->solverInfo);
  }

  /* Update absolute time for base rate */
  /* The "clockTick0" counts the number of times the code of this task has
   * been executed. The absolute time is the multiplication of "clockTick0"
   * and "Timing.stepSize0". Size of "clockTick0" ensures timer will not
   * overflow during the application lifespan selected.
   * Timer of this task consists of two 32 bit unsigned integers.
   * The two integers represent the low bits Timing.clockTick0 and the high bits
   * Timing.clockTickH0. When the low bit overflows to 0, the high bits increment.
   */
  if (!(++compilation_1_sm_computation_M->Timing.clockTick0)) {
    ++compilation_1_sm_computation_M->Timing.clockTickH0;
  }

  compilation_1_sm_computation_M->Timing.t[0] = rtsiGetSolverStopTime
    (&compilation_1_sm_computation_M->solverInfo);

  {
    /* Update absolute timer for sample time: [0.001s, 0.0s] */
    /* The "clockTick1" counts the number of times the code of this task has
     * been executed. The absolute time is the multiplication of "clockTick1"
     * and "Timing.stepSize1". Size of "clockTick1" ensures timer will not
     * overflow during the application lifespan selected.
     * Timer of this task consists of two 32 bit unsigned integers.
     * The two integers represent the low bits Timing.clockTick1 and the high bits
     * Timing.clockTickH1. When the low bit overflows to 0, the high bits increment.
     */
    if (!(++compilation_1_sm_computation_M->Timing.clockTick1)) {
      ++compilation_1_sm_computation_M->Timing.clockTickH1;
    }

    compilation_1_sm_computation_M->Timing.t[1] =
      compilation_1_sm_computation_M->Timing.clockTick1 *
      compilation_1_sm_computation_M->Timing.stepSize1 +
      compilation_1_sm_computation_M->Timing.clockTickH1 *
      compilation_1_sm_computation_M->Timing.stepSize1 * 4294967296.0;
  }

  /* tid is required for a uniform function interface.
   * Argument tid is not used in the function. */
  UNUSED_PARAMETER(tid);
}

/* Derivatives for root system: '<Root>' */
void compilation_1_sm_computation_derivatives(void)
{
  /* Derivatives for Integrator: '<S2>/Integrator3' */
  {
    boolean_T lsat;
    boolean_T usat;
    lsat = ( compilation_1_sm_computation_X.Integrator3_CSTATE <=
            compilation_1_sm_computation_P.Integrator3_LowerSat );
    usat = ( compilation_1_sm_computation_X.Integrator3_CSTATE >=
            compilation_1_sm_computation_P.Integrator3_UpperSat );
    if ((!lsat && !usat) ||
        (lsat && (compilation_1_sm_computation_B.plantresponse > 0)) ||
        (usat && (compilation_1_sm_computation_B.plantresponse < 0)) ) {
      ((StateDerivatives_compilation_1_sm_computation *)
        compilation_1_sm_computation_M->ModelData.derivs)->Integrator3_CSTATE =
        compilation_1_sm_computation_B.plantresponse;
    } else {
      /* in saturation */
      ((StateDerivatives_compilation_1_sm_computation *)
        compilation_1_sm_computation_M->ModelData.derivs)->Integrator3_CSTATE =
        0.0;
    }
  }

  /* Derivatives for Integrator: '<S2>/Integrator1' */
  ((StateDerivatives_compilation_1_sm_computation *)
    compilation_1_sm_computation_M->ModelData.derivs)->Integrator1_CSTATE =
    compilation_1_sm_computation_B.Error;

  /* Derivatives for Integrator: '<S2>/Integrator2' */
  ((StateDerivatives_compilation_1_sm_computation *)
    compilation_1_sm_computation_M->ModelData.derivs)->Integrator2_CSTATE =
    compilation_1_sm_computation_B.Gain;
}

/* Model initialize function */
void compilation_1_sm_computation_initialize(boolean_T firstTime)
{
  (void)firstTime;

  /* Registration code */

  /* initialize non-finites */
  rt_InitInfAndNaN(sizeof(real_T));

  /* initialize real-time model */
  (void) memset((void *)compilation_1_sm_computation_M, 0,
                sizeof(RT_MODEL_compilation_1_sm_computation));

  {
    /* Setup solver object */
    rtsiSetSimTimeStepPtr(&compilation_1_sm_computation_M->solverInfo,
                          &compilation_1_sm_computation_M->Timing.simTimeStep);
    rtsiSetTPtr(&compilation_1_sm_computation_M->solverInfo, &rtmGetTPtr
                (compilation_1_sm_computation_M));
    rtsiSetStepSizePtr(&compilation_1_sm_computation_M->solverInfo,
                       &compilation_1_sm_computation_M->Timing.stepSize0);
    rtsiSetdXPtr(&compilation_1_sm_computation_M->solverInfo,
                 &compilation_1_sm_computation_M->ModelData.derivs);
    rtsiSetContStatesPtr(&compilation_1_sm_computation_M->solverInfo,
                         &compilation_1_sm_computation_M->ModelData.contStates);
    rtsiSetNumContStatesPtr(&compilation_1_sm_computation_M->solverInfo,
      &compilation_1_sm_computation_M->Sizes.numContStates);
    rtsiSetErrorStatusPtr(&compilation_1_sm_computation_M->solverInfo,
                          (&rtmGetErrorStatus(compilation_1_sm_computation_M)));
    rtsiSetRTModelPtr(&compilation_1_sm_computation_M->solverInfo,
                      compilation_1_sm_computation_M);
  }

  rtsiSetSimTimeStep(&compilation_1_sm_computation_M->solverInfo,
                     MAJOR_TIME_STEP);
  compilation_1_sm_computation_M->ModelData.intgData.y =
    compilation_1_sm_computation_M->ModelData.odeY;
  compilation_1_sm_computation_M->ModelData.intgData.f[0] =
    compilation_1_sm_computation_M->ModelData.odeF[0];
  compilation_1_sm_computation_M->ModelData.intgData.f[1] =
    compilation_1_sm_computation_M->ModelData.odeF[1];
  compilation_1_sm_computation_M->ModelData.intgData.f[2] =
    compilation_1_sm_computation_M->ModelData.odeF[2];
  compilation_1_sm_computation_M->ModelData.intgData.f[3] =
    compilation_1_sm_computation_M->ModelData.odeF[3];
  compilation_1_sm_computation_M->ModelData.contStates = ((real_T *)
    &compilation_1_sm_computation_X);
  rtsiSetSolverData(&compilation_1_sm_computation_M->solverInfo, (void *)
                    &compilation_1_sm_computation_M->ModelData.intgData);
  rtsiSetSolverName(&compilation_1_sm_computation_M->solverInfo,"ode4");
  compilation_1_sm_computation_M->solverInfoPtr =
    (&compilation_1_sm_computation_M->solverInfo);

  /* Initialize timing info */
  {
    int_T *mdlTsMap =
      compilation_1_sm_computation_M->Timing.sampleTimeTaskIDArray;
    mdlTsMap[0] = 0;
    mdlTsMap[1] = 1;
    compilation_1_sm_computation_M->Timing.sampleTimeTaskIDPtr = (&mdlTsMap[0]);
    compilation_1_sm_computation_M->Timing.sampleTimes =
      (&compilation_1_sm_computation_M->Timing.sampleTimesArray[0]);
    compilation_1_sm_computation_M->Timing.offsetTimes =
      (&compilation_1_sm_computation_M->Timing.offsetTimesArray[0]);

    /* task periods */
    compilation_1_sm_computation_M->Timing.sampleTimes[0] = (0.0);
    compilation_1_sm_computation_M->Timing.sampleTimes[1] = (0.001);

    /* task offsets */
    compilation_1_sm_computation_M->Timing.offsetTimes[0] = (0.0);
    compilation_1_sm_computation_M->Timing.offsetTimes[1] = (0.0);
  }

  rtmSetTPtr(compilation_1_sm_computation_M,
             &compilation_1_sm_computation_M->Timing.tArray[0]);

  {
    int_T *mdlSampleHits = compilation_1_sm_computation_M->Timing.sampleHitArray;
    mdlSampleHits[0] = 1;
    mdlSampleHits[1] = 1;
    compilation_1_sm_computation_M->Timing.sampleHits = (&mdlSampleHits[0]);
  }

  rtmSetTFinal(compilation_1_sm_computation_M, -1);
  compilation_1_sm_computation_M->Timing.stepSize0 = 0.001;
  compilation_1_sm_computation_M->Timing.stepSize1 = 0.001;

  /* Setup for data logging */
  {
    static RTWLogInfo rt_DataLoggingInfo;
    compilation_1_sm_computation_M->rtwLogInfo = &rt_DataLoggingInfo;
  }

  /* Setup for data logging */
  {
    rtliSetLogXSignalInfo(compilation_1_sm_computation_M->rtwLogInfo, (NULL));
    rtliSetLogXSignalPtrs(compilation_1_sm_computation_M->rtwLogInfo, (NULL));
    rtliSetLogT(compilation_1_sm_computation_M->rtwLogInfo, "");
    rtliSetLogX(compilation_1_sm_computation_M->rtwLogInfo, "");
    rtliSetLogXFinal(compilation_1_sm_computation_M->rtwLogInfo, "");
    rtliSetSigLog(compilation_1_sm_computation_M->rtwLogInfo, "");
    rtliSetLogVarNameModifier(compilation_1_sm_computation_M->rtwLogInfo, "rt_");
    rtliSetLogFormat(compilation_1_sm_computation_M->rtwLogInfo, 0);
    rtliSetLogMaxRows(compilation_1_sm_computation_M->rtwLogInfo, 1000);
    rtliSetLogDecimation(compilation_1_sm_computation_M->rtwLogInfo, 1);
    rtliSetLogY(compilation_1_sm_computation_M->rtwLogInfo, "");
    rtliSetLogYSignalInfo(compilation_1_sm_computation_M->rtwLogInfo, (NULL));
    rtliSetLogYSignalPtrs(compilation_1_sm_computation_M->rtwLogInfo, (NULL));
  }

  compilation_1_sm_computation_M->solverInfoPtr =
    (&compilation_1_sm_computation_M->solverInfo);
  compilation_1_sm_computation_M->Timing.stepSize = (0.001);
  rtsiSetFixedStepSize(&compilation_1_sm_computation_M->solverInfo, 0.001);
  rtsiSetSolverMode(&compilation_1_sm_computation_M->solverInfo,
                    SOLVER_MODE_SINGLETASKING);

  /* block I/O */
  compilation_1_sm_computation_M->ModelData.blockIO = ((void *)
    &compilation_1_sm_computation_B);

  {
    compilation_1_sm_computation_B.Sum = 0.0;
    compilation_1_sm_computation_B.SFunction = 0.0;
    compilation_1_sm_computation_B.d = 0.0;
    compilation_1_sm_computation_B.Error = 0.0;
    compilation_1_sm_computation_B.Gain1 = 0.0;
    compilation_1_sm_computation_B.c = 0.0;
    compilation_1_sm_computation_B.e = 0.0;
    compilation_1_sm_computation_B.Gain = 0.0;
    compilation_1_sm_computation_B.plantresponse = 0.0;
  }

  /* parameters */
  compilation_1_sm_computation_M->ModelData.defaultParam = ((real_T *)
    &compilation_1_sm_computation_P);

  /* states (continuous) */
  {
    real_T *x = (real_T *) &compilation_1_sm_computation_X;
    compilation_1_sm_computation_M->ModelData.contStates = (x);
    (void) memset((void *)&compilation_1_sm_computation_X, 0,
                  sizeof(ContinuousStates_compilation_1_sm_computation));
  }

  /* states (dwork) */
  compilation_1_sm_computation_M->Work.dwork = ((void *)
    &compilation_1_sm_computation_DWork);
  (void) memset((void *)&compilation_1_sm_computation_DWork, 0,
                sizeof(D_Work_compilation_1_sm_computation));
  compilation_1_sm_computation_DWork.SFunction_PreviousInput = 0.0;
  compilation_1_sm_computation_DWork.Sensorresponsetime_RWORK.modelTStart = 0.0;

  {
    int_T i;
    for (i = 0; i < 2048; i++) {
      compilation_1_sm_computation_DWork.Sensorresponsetime_RWORK.TUbufferArea[i]
        = 0.0;
    }
  }

  compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampA = 0.0;
  compilation_1_sm_computation_DWork.Derivative1_RWORK.LastUAtTimeA = 0.0;
  compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampB = 0.0;
  compilation_1_sm_computation_DWork.Derivative1_RWORK.LastUAtTimeB = 0.0;
  compilation_1_sm_computation_DWork.Actuatorresponsetime_RWORK.modelTStart =
    0.0;

  {
    int_T i;
    for (i = 0; i < 2048; i++) {
      compilation_1_sm_computation_DWork.Actuatorresponsetime_RWORK.TUbufferArea[
        i] = 0.0;
    }
  }

  /* child S-Function registration */
  {
    RTWSfcnInfo *sfcnInfo =
      &compilation_1_sm_computation_M->NonInlinedSFcns.sfcnInfo;
    compilation_1_sm_computation_M->sfcnInfo = (sfcnInfo);
    rtssSetErrorStatusPtr(sfcnInfo, (&rtmGetErrorStatus
      (compilation_1_sm_computation_M)));
    rtssSetNumRootSampTimesPtr(sfcnInfo,
      &compilation_1_sm_computation_M->Sizes.numSampTimes);
    compilation_1_sm_computation_M->NonInlinedSFcns.taskTimePtrs[0] =
      &(rtmGetTPtr(compilation_1_sm_computation_M)[0]);
    compilation_1_sm_computation_M->NonInlinedSFcns.taskTimePtrs[1] =
      &(rtmGetTPtr(compilation_1_sm_computation_M)[1]);
    rtssSetTPtrPtr(sfcnInfo,
                   compilation_1_sm_computation_M->NonInlinedSFcns.taskTimePtrs);
    rtssSetTStartPtr(sfcnInfo, &rtmGetTStart(compilation_1_sm_computation_M));
    rtssSetTFinalPtr(sfcnInfo, &rtmGetTFinal(compilation_1_sm_computation_M));
    rtssSetTimeOfLastOutputPtr(sfcnInfo, &rtmGetTimeOfLastOutput
      (compilation_1_sm_computation_M));
    rtssSetStepSizePtr(sfcnInfo,
                       &compilation_1_sm_computation_M->Timing.stepSize);
    rtssSetStopRequestedPtr(sfcnInfo, &rtmGetStopRequested
      (compilation_1_sm_computation_M));
    rtssSetDerivCacheNeedsResetPtr(sfcnInfo,
      &compilation_1_sm_computation_M->ModelData.derivCacheNeedsReset);
    rtssSetZCCacheNeedsResetPtr(sfcnInfo,
      &compilation_1_sm_computation_M->ModelData.zCCacheNeedsReset);
    rtssSetBlkStateChangePtr(sfcnInfo,
      &compilation_1_sm_computation_M->ModelData.blkStateChange);
    rtssSetSampleHitsPtr(sfcnInfo,
                         &compilation_1_sm_computation_M->Timing.sampleHits);
    rtssSetPerTaskSampleHitsPtr(sfcnInfo,
      &compilation_1_sm_computation_M->Timing.perTaskSampleHits);
    rtssSetSimModePtr(sfcnInfo, &compilation_1_sm_computation_M->simMode);
    rtssSetSolverInfoPtr(sfcnInfo,
                         &compilation_1_sm_computation_M->solverInfoPtr);
  }

  compilation_1_sm_computation_M->Sizes.numSFcns = (2);

  /* register each child */
  {
    (void) memset((void *)
                  &compilation_1_sm_computation_M->NonInlinedSFcns.childSFunctions
                  [0], 0,
                  2*sizeof(SimStruct));
    compilation_1_sm_computation_M->childSfunctions =
      (&compilation_1_sm_computation_M->NonInlinedSFcns.childSFunctionPtrs[0]);
    compilation_1_sm_computation_M->childSfunctions[0] =
      (&compilation_1_sm_computation_M->NonInlinedSFcns.childSFunctions[0]);
    compilation_1_sm_computation_M->childSfunctions[1] =
      (&compilation_1_sm_computation_M->NonInlinedSFcns.childSFunctions[1]);

    /* Level2 S-Function Block: compilation_1_sm_computation/<S5>/S-Function (RECV_Param) */
    {
      SimStruct *rts = compilation_1_sm_computation_M->childSfunctions[0];

      /* timing info */
      time_T *sfcnPeriod =
        compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn0.sfcnPeriod;
      time_T *sfcnOffset =
        compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn0.sfcnOffset;
      int_T *sfcnTsMap =
        compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn0.sfcnTsMap;
      (void) memset((void*)sfcnPeriod, 0,
                    sizeof(time_T)*1);
      (void) memset((void*)sfcnOffset, 0,
                    sizeof(time_T)*1);
      ssSetSampleTimePtr(rts, &sfcnPeriod[0]);
      ssSetOffsetTimePtr(rts, &sfcnOffset[0]);
      ssSetSampleTimeTaskIDPtr(rts, sfcnTsMap);

      /* Set up the mdlInfo pointer */
      {
        ssSetBlkInfo2Ptr(rts,
                         &compilation_1_sm_computation_M->NonInlinedSFcns.blkInfo2
                         [0]);
      }

      ssSetRTWSfcnInfo(rts, compilation_1_sm_computation_M->sfcnInfo);

      /* Allocate memory of model methods 2 */
      {
        ssSetModelMethods2(rts,
                           &compilation_1_sm_computation_M->NonInlinedSFcns.methods2
                           [0]);
      }

      /* Allocate memory of model methods 3 */
      {
        ssSetModelMethods3(rts,
                           &compilation_1_sm_computation_M->NonInlinedSFcns.methods3
                           [0]);
      }

      /* Allocate memory for states auxilliary information */
      {
        ssSetStatesInfo2(rts,
                         &compilation_1_sm_computation_M->NonInlinedSFcns.statesInfo2
                         [0]);
      }

      /* outputs */
      {
        ssSetPortInfoForOutputs(rts,
          &compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn0.outputPortInfo
          [0]);
        _ssSetNumOutputPorts(rts, 1);

        /* port 0 */
        {
          _ssSetOutputPortNumDimensions(rts, 0, 1);
          ssSetOutputPortWidth(rts, 0, 1);
          ssSetOutputPortSignal(rts, 0, ((real_T *)
            &compilation_1_sm_computation_B.SFunction));
        }
      }

      /* path info */
      ssSetModelName(rts, "S-Function");
      ssSetPath(rts,
                "compilation_1_sm_computation/sm_computation/OpComm/Receive/S-Function");
      ssSetRTModel(rts,compilation_1_sm_computation_M);
      ssSetParentSS(rts, (NULL));
      ssSetRootSS(rts, rts);
      ssSetVersion(rts, SIMSTRUCT_VERSION_LEVEL2);

      /* parameters */
      {
        mxArray **sfcnParams = (mxArray **)
          &compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn0.params;
        ssSetSFcnParamsCount(rts, 2);
        ssSetSFcnParamsPtr(rts, &sfcnParams[0]);
        ssSetSFcnParam(rts, 0, (mxArray*)
                       compilation_1_sm_computation_P.SFunction_P1_Size);
        ssSetSFcnParam(rts, 1, (mxArray*)
                       compilation_1_sm_computation_P.SFunction_P2_Size);
      }

      /* registration */
      RECV_Param(rts);
      sfcnInitializeSizes(rts);
      sfcnInitializeSampleTimes(rts);

      /* adjust sample time */
      ssSetSampleTime(rts, 0, 0.001);
      ssSetOffsetTime(rts, 0, 0.0);
      sfcnTsMap[0] = 1;

      /* set compiled values of dynamic vector attributes */
      ssSetNumNonsampledZCs(rts, 0);

      /* Update connectivity flags for each port */
      _ssSetOutputPortConnected(rts, 0, 1);
      _ssSetOutputPortBeingMerged(rts, 0, 0);

      /* Update the BufferDstPort flags for each input port */
    }

    /* Level2 S-Function Block: compilation_1_sm_computation/<S9>/S-Function (OP_SEND) */
    {
      SimStruct *rts = compilation_1_sm_computation_M->childSfunctions[1];

      /* timing info */
      time_T *sfcnPeriod =
        compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn1.sfcnPeriod;
      time_T *sfcnOffset =
        compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn1.sfcnOffset;
      int_T *sfcnTsMap =
        compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn1.sfcnTsMap;
      (void) memset((void*)sfcnPeriod, 0,
                    sizeof(time_T)*1);
      (void) memset((void*)sfcnOffset, 0,
                    sizeof(time_T)*1);
      ssSetSampleTimePtr(rts, &sfcnPeriod[0]);
      ssSetOffsetTimePtr(rts, &sfcnOffset[0]);
      ssSetSampleTimeTaskIDPtr(rts, sfcnTsMap);

      /* Set up the mdlInfo pointer */
      {
        ssSetBlkInfo2Ptr(rts,
                         &compilation_1_sm_computation_M->NonInlinedSFcns.blkInfo2
                         [1]);
      }

      ssSetRTWSfcnInfo(rts, compilation_1_sm_computation_M->sfcnInfo);

      /* Allocate memory of model methods 2 */
      {
        ssSetModelMethods2(rts,
                           &compilation_1_sm_computation_M->NonInlinedSFcns.methods2
                           [1]);
      }

      /* Allocate memory of model methods 3 */
      {
        ssSetModelMethods3(rts,
                           &compilation_1_sm_computation_M->NonInlinedSFcns.methods3
                           [1]);
      }

      /* Allocate memory for states auxilliary information */
      {
        ssSetStatesInfo2(rts,
                         &compilation_1_sm_computation_M->NonInlinedSFcns.statesInfo2
                         [1]);
      }

      /* inputs */
      {
        _ssSetNumInputPorts(rts, 1);
        ssSetPortInfoForInputs(rts,
          &compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn1.inputPortInfo[0]);

        /* port 0 */
        {
          real_T const **sfcnUPtrs = (real_T const **)
            &compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn1.UPtrs0;
          sfcnUPtrs[0] = &compilation_1_sm_computation_B.SFunction;
          sfcnUPtrs[1] = &compilation_1_sm_computation_B.d;
          sfcnUPtrs[2] = &compilation_1_sm_computation_B.c;
          sfcnUPtrs[3] = &compilation_1_sm_computation_B.e;
          ssSetInputPortSignalPtrs(rts, 0, (InputPtrsType)&sfcnUPtrs[0]);
          _ssSetInputPortNumDimensions(rts, 0, 1);
          ssSetInputPortWidth(rts, 0, 4);
        }
      }

      /* path info */
      ssSetModelName(rts, "S-Function");
      ssSetPath(rts,
                "compilation_1_sm_computation/sm_computation/rtlab_send_subsystem/Subsystem1/Send1/S-Function");
      ssSetRTModel(rts,compilation_1_sm_computation_M);
      ssSetParentSS(rts, (NULL));
      ssSetRootSS(rts, rts);
      ssSetVersion(rts, SIMSTRUCT_VERSION_LEVEL2);

      /* parameters */
      {
        mxArray **sfcnParams = (mxArray **)
          &compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn1.params;
        ssSetSFcnParamsCount(rts, 1);
        ssSetSFcnParamsPtr(rts, &sfcnParams[0]);
        ssSetSFcnParam(rts, 0, (mxArray*)
                       compilation_1_sm_computation_P.SFunction_P1_Size_d);
      }

      /* work vectors */
      ssSetIWork(rts, (int_T *)
                 &compilation_1_sm_computation_DWork.SFunction_IWORK[0]);

      {
        struct _ssDWorkRecord *dWorkRecord = (struct _ssDWorkRecord *)
          &compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn1.dWork;
        struct _ssDWorkAuxRecord *dWorkAuxRecord = (struct _ssDWorkAuxRecord *)
          &compilation_1_sm_computation_M->NonInlinedSFcns.Sfcn1.dWorkAux;
        ssSetSFcnDWork(rts, dWorkRecord);
        ssSetSFcnDWorkAux(rts, dWorkAuxRecord);
        _ssSetNumDWork(rts, 1);

        /* IWORK */
        ssSetDWorkWidth(rts, 0, 5);
        ssSetDWorkDataType(rts, 0,SS_INTEGER);
        ssSetDWorkComplexSignal(rts, 0, 0);
        ssSetDWork(rts, 0, &compilation_1_sm_computation_DWork.SFunction_IWORK[0]);
      }

      /* registration */
      OP_SEND(rts);
      sfcnInitializeSizes(rts);
      sfcnInitializeSampleTimes(rts);

      /* adjust sample time */
      ssSetSampleTime(rts, 0, 0.001);
      ssSetOffsetTime(rts, 0, 0.0);
      sfcnTsMap[0] = 1;

      /* set compiled values of dynamic vector attributes */
      ssSetInputPortWidth(rts, 0, 4);
      ssSetInputPortDataType(rts, 0, SS_DOUBLE);
      ssSetInputPortComplexSignal(rts, 0, 0);
      ssSetInputPortFrameData(rts, 0, 0);
      ssSetNumNonsampledZCs(rts, 0);

      /* Update connectivity flags for each port */
      _ssSetInputPortConnected(rts, 0, 1);

      /* Update the BufferDstPort flags for each input port */
      ssSetInputPortBufferDstPort(rts, 0, -1);
    }
  }
}

/* Model terminate function */
void compilation_1_sm_computation_terminate(void)
{
  /* Level2 S-Function Block: '<S5>/S-Function' (RECV_Param) */
  {
    SimStruct *rts = compilation_1_sm_computation_M->childSfunctions[0];
    sfcnTerminate(rts);
  }

  /* Level2 S-Function Block: '<S9>/S-Function' (OP_SEND) */
  {
    SimStruct *rts = compilation_1_sm_computation_M->childSfunctions[1];
    sfcnTerminate(rts);
  }
}

/*========================================================================*
 * Start of GRT compatible call interface                                 *
 *========================================================================*/

/* Solver interface called by GRT_Main */
#ifndef USE_GENERATED_SOLVER

void rt_ODECreateIntegrationData(RTWSolverInfo *si)
{
  UNUSED_PARAMETER(si);
  return;
}                                      /* do nothing */

void rt_ODEDestroyIntegrationData(RTWSolverInfo *si)
{
  UNUSED_PARAMETER(si);
  return;
}                                      /* do nothing */

void rt_ODEUpdateContinuousStates(RTWSolverInfo *si)
{
  UNUSED_PARAMETER(si);
  return;
}                                      /* do nothing */

#endif

void MdlOutputs(int_T tid)
{
  compilation_1_sm_computation_output(tid);
}

void MdlUpdate(int_T tid)
{
  compilation_1_sm_computation_update(tid);
}

void MdlInitializeSizes(void)
{
  compilation_1_sm_computation_M->Sizes.numContStates = (3);/* Number of continuous states */
  compilation_1_sm_computation_M->Sizes.numY = (0);/* Number of model outputs */
  compilation_1_sm_computation_M->Sizes.numU = (0);/* Number of model inputs */
  compilation_1_sm_computation_M->Sizes.sysDirFeedThru = (0);/* The model is not direct feedthrough */
  compilation_1_sm_computation_M->Sizes.numSampTimes = (2);/* Number of sample times */
  compilation_1_sm_computation_M->Sizes.numBlocks = (20);/* Number of blocks */
  compilation_1_sm_computation_M->Sizes.numBlockIO = (9);/* Number of block outputs */
  compilation_1_sm_computation_M->Sizes.numBlockPrms = (25);/* Sum of parameter "widths" */
}

void MdlInitializeSampleTimes(void)
{
}

void MdlInitialize(void)
{
  /* user code (Initialize function Body) */

  /* System '<Root>' */
  /* Opal-RT Technologies */
  opalSizeDwork = sizeof(rtDWork);
  if (Opal_rtmGetNumBlockIO(pRtModel) != 0)
    opalSizeBlockIO = sizeof(rtB);
  else
    opalSizeBlockIO = 0;
  if (Opal_rtmGetNumBlockParams(pRtModel) != 0)
    opalSizeRTP = sizeof(rtP);
  else
    opalSizeRTP = 0;

  /* InitializeConditions for Memory: '<S1>/S-Function' */
  compilation_1_sm_computation_DWork.SFunction_PreviousInput =
    compilation_1_sm_computation_P.SFunction_X0;

  /* Level2 S-Function Block: '<S5>/S-Function' (RECV_Param) */
  {
    SimStruct *rts = compilation_1_sm_computation_M->childSfunctions[0];
    sfcnInitializeConditions(rts);
    if (ssGetErrorStatus(rts) != (NULL))
      return;
  }

  /* InitializeConditions for Integrator: '<S2>/Integrator3' */
  compilation_1_sm_computation_X.Integrator3_CSTATE =
    compilation_1_sm_computation_P.Integrator3_IC;

  /* InitializeConditions for Integrator: '<S2>/Integrator1' */
  compilation_1_sm_computation_X.Integrator1_CSTATE =
    compilation_1_sm_computation_P.Integrator1_IC;

  /* InitializeConditions for Derivative: '<S2>/Derivative1' */
  compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampA = rtInf;
  compilation_1_sm_computation_DWork.Derivative1_RWORK.TimeStampB = rtInf;

  /* Level2 S-Function Block: '<S9>/S-Function' (OP_SEND) */
  {
    SimStruct *rts = compilation_1_sm_computation_M->childSfunctions[1];
    sfcnInitializeConditions(rts);
    if (ssGetErrorStatus(rts) != (NULL))
      return;
  }

  /* InitializeConditions for Integrator: '<S2>/Integrator2' */
  compilation_1_sm_computation_X.Integrator2_CSTATE =
    compilation_1_sm_computation_P.Integrator2_IC;
}

void MdlStart(void)
{
  /* Start for TransportDelay: '<S2>/Sensor response time' */
  {
    real_T *pBuffer =
      &compilation_1_sm_computation_DWork.Sensorresponsetime_RWORK.TUbufferArea
      [0];
    compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Tail = 0;
    compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Head = 0;
    compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.Last = 0;
    compilation_1_sm_computation_DWork.Sensorresponsetime_IWORK.CircularBufSize =
      1024;
    pBuffer[0] = compilation_1_sm_computation_P.Sensorresponsetime_InitOutput;
    pBuffer[1024] = compilation_1_sm_computation_M->Timing.t[0];
    compilation_1_sm_computation_DWork.Sensorresponsetime_PWORK.TUbufferPtrs[0] =
      (void *) &pBuffer[0];
    compilation_1_sm_computation_DWork.Sensorresponsetime_PWORK.TUbufferPtrs[1] =
      (void *) &pBuffer[1024];
  }

  /* Start for TransportDelay: '<S2>/Actuator response time' */
  {
    real_T *pBuffer =
      &compilation_1_sm_computation_DWork.Actuatorresponsetime_RWORK.TUbufferArea
      [0];
    compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Tail = 0;
    compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Head = 0;
    compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.Last = 0;
    compilation_1_sm_computation_DWork.Actuatorresponsetime_IWORK.CircularBufSize
      = 1024;
    pBuffer[0] = compilation_1_sm_computation_P.Actuatorresponsetime_InitOutput;
    pBuffer[1024] = compilation_1_sm_computation_M->Timing.t[0];
    compilation_1_sm_computation_DWork.Actuatorresponsetime_PWORK.TUbufferPtrs[0]
      = (void *) &pBuffer[0];
    compilation_1_sm_computation_DWork.Actuatorresponsetime_PWORK.TUbufferPtrs[1]
      = (void *) &pBuffer[1024];
  }

  MdlInitialize();
}

void MdlTerminate(void)
{
  compilation_1_sm_computation_terminate();
}

RT_MODEL_compilation_1_sm_computation *compilation_1_sm_computation(void)
{
  compilation_1_sm_computation_initialize(1);
  return compilation_1_sm_computation_M;
}

/*========================================================================*
 * End of GRT compatible call interface                                   *
 *========================================================================*/
