#include "pythonInterpreter.h"

void pythonExchangeValuesCymdistNoModelica(const char * moduleName,
                          const char * functionName,
						  double * modNamRef,
						  const size_t nDblWri, 
						  const char ** strWri, 
						  double * dblValWri, 
						  size_t nDblRea, 
						  const char ** strRea,
						  double * dblValRea, 
						  size_t nDblParWri, 
						  const char ** strParWri, 
						  double * dblValParWri, 
						  double *resWri,
			              void (*ModelicaFormatError)(const char *string,...))
{
  PyObject *pName, *pModule, *pFunc;
  PyObject *pArgsDbl,  *pArgsInt, *pArgsStr;
  PyObject *pArgs, *pValue;
  Py_ssize_t pIndVal;
  PyObject *pItemDbl;
  char* arg="";
  Py_ssize_t nStrWri = 0;
  Py_ssize_t nStrRea = 0;
  Py_ssize_t nStrLocRea = 0;
  Py_ssize_t nStrParWri = 0;
  Py_ssize_t i;
  Py_ssize_t iArg = 0;
  /* The number of arguments starts*/
  /* at 2 since we always have the */
  /* reference value to a CYMDIST  */
  /* model and a flag to indicate */
  /* if results should be writtens.*/
  /* as argument*/
  Py_ssize_t nArg = 2;
  Py_ssize_t iRet = 0;
  Py_ssize_t nRet = 0;
  /*//////////////////////////////////////////////////////////////////////////*/
  /* Initialize Python interpreter*/
  Py_Initialize();
  /* Set the entries for sys.argv.*/
  /* This is required if a script uses sys.argv, such as bacpypes.*/
  /* See also http://stackoverflow.com/questions/19381441/python-modelica-connection-fails-due-to-import-error*/
  PySys_SetArgv(0, &arg);


  /*//////////////////////////////////////////////////////////////////////////*/
  /* Load Python module*/
  pName = PyUnicode_FromString(moduleName);
  if (!pName) {
    (*ModelicaFormatError)("Failed to convert moduleName '%s' to Python object.\n", moduleName);
  }

  pModule = PyImport_Import(pName);
  Py_DECREF(pName);
  if (!pModule) {
    /*    PyErr_Print();*/
    PyObject *pValue, *pType, *pTraceBack;
    PyErr_Fetch(&pType, &pValue, &pTraceBack);
    if (pType != NULL)
      Py_DECREF(pType);
    if (pTraceBack != NULL)
      Py_DECREF(pTraceBack);
    /* Py_Finalize(); // removed, see note at other Py_Finalize() statement*/
    (*ModelicaFormatError)("Failed to load \"%s\".\n\
This may occur if you did not set the PYTHONPATH environment variable\n\
or if the Python module contains a syntax error.\n\
The error message is \"%s\"",
                        moduleName,
                        PyBytes_AsString(PyObject_Repr(pValue)));
  }

  /*//////////////////////////////////////////////////////////////////////////*/
  /* Python module is successfully loaded.*/
  /* Load function*/
  pFunc = PyObject_GetAttrString(pModule, functionName);
  /* pFunc is a new reference */

  if (!(pFunc && PyCallable_Check(pFunc))){
    if (PyErr_Occurred())
      PyErr_Print();
    /* Py_Finalize(); // removed, see note at other Py_Finalize() statement*/
    (*ModelicaFormatError)(
			"Cannot find function \"%s\".\nMake sure PYTHONPATH contains the path of the module that contains this function.\n",
			functionName);

  }

  /*//////////////////////////////////////////////////////////////////////////*/
  /* The function is loaded.*/
  /*//////////////////////////////////////////////////////////////////////////*/
  /* Create arguments for the python function*/
  if (nDblWri > 0){
	  /* Increase the number of arguments to 2*/
	  /* One is for the vector of input names*/
	  /* to be sent to CYMDISTToFMU, the second one is*/
	  /* for the vector of input values to be sent*/
	  /* to CYMDISTToFMU.*/
	  nStrWri = nDblWri;
	  nArg = nArg + 2;
  }
  if (nDblRea > 0){
	  /* Increase the number of argument to 1*/
	  /* This is for the vector of output names.*/
	  nStrRea = nDblRea;
	  nArg=nArg+1;
  }
  if (nDblParWri > 0){
	  /* Increase the number of arguments to 2*/
	  /* One is for the vector of strings parameters*/
	  /* to be sent to CYMDISTToFMU, the second one is */
	  /* for the vector of parameter values to be sent*/
	  /* to CYMDISTToFMU.*/
	  nStrParWri = nDblParWri;
	  nArg = nArg + 2;
  }

  if (nArg > 0)
    pArgs = PyTuple_New(nArg);
  else
    pArgs = NULL;

  /* Convert the arguments*/
  /* a) Convert double[]*/
  pArgsDbl = PyList_New(1);
  /* Convert argument to a python float*/
  pValue = PyFloat_FromDouble(modNamRef[0]);
  if (!pValue) {
	  /* Failed to convert argument.*/
	  Py_DECREF(pArgsDbl);
	  Py_DECREF(pModule);
	  /* According to the Modelica specification,*/
	  /* the function ModelicaError never returns to the calling function.*/
	  (*ModelicaFormatError)("Cannot convert double argument %f for model name to Python format.", modNamRef[0]);
  }
  /* pValue reference stolen here*/
  PyList_SetItem(pArgsDbl, 0, pValue);
  /* If there is only a scalar double, then don't build a list.*/
  /* Just put the scalar value into the list of arguments*/
  PyTuple_SetItem(pArgs, iArg, PyList_GetItem(pArgsDbl, (Py_ssize_t)0));
  iArg++;

  /* b) Convert double[]*/
  if ( nDblWri > 0 ){
    pArgsDbl = PyList_New(nDblWri);
    for (i = 0; i < nDblWri; ++i) {
      /* Convert argument to a python float*/
      pValue = PyFloat_FromDouble(dblValWri[i]);
      if (!pValue) {
	/* Failed to convert argument.*/
	Py_DECREF(pArgsDbl);
	Py_DECREF(pModule);
	/* According to the Modelica specification,*/
	/* the function ModelicaError never returns to the calling function.*/
	(*ModelicaFormatError)("Cannot convert double argument number %i to Python format.", i);
      }
      /* pValue reference stolen here*/
      PyList_SetItem(pArgsDbl, i, pValue);
    }
    /* If there is only a scalar double, then don't build a list.*/
    /* Just put the scalar value into the list of arguments*/
    if ( nDblWri == 1)
      PyTuple_SetItem(pArgs, iArg, PyList_GetItem(pArgsDbl, (Py_ssize_t)0));
    else
      PyTuple_SetItem(pArgs, iArg, pArgsDbl);
    iArg++;
  }
  
    /* c) Convert char **, an array of character arrays*/
  if ( nStrWri > 0 ){
    pArgsStr = PyList_New(nStrWri);

    for (i = 0; i < nStrWri; ++i) {
      /* Convert argument to a python float*/
      /*      Py_ssize_t len = 0;*/
      /* According to the Modelica Specification, strings are terminated by '\0'*/
      /* Seek the string length*/
      /*      while (strWri[i][len] != '\0')*/
      /*	len++;*/

      /*      pValue = PyUnicode_FromStringAndSize(strWri[i], len);*/
      pValue = PyUnicode_FromString(strWri[i]);
      if (!pValue) {
	/* Failed to convert argument.*/
	Py_DECREF(pArgsStr);
	Py_DECREF(pModule);
	/* According to the Modelica specification,*/
	/* the function ModelicaError never returns to the calling function.*/
	(*ModelicaFormatError)("Cannot convert string argument number %i to Python format.", i);
      }
      /* pValue reference stolen here*/
      PyList_SetItem(pArgsStr, i, pValue);
    }
    /* If there is only a scalar string, then don't build a list.*/
    /* Just put the scalar value into the list of arguments.*/
    if ( nStrWri == 1)
	PyTuple_SetItem(pArgs, iArg, PyList_GetItem(pArgsStr, (Py_ssize_t)0));
      else
	PyTuple_SetItem(pArgs, iArg, pArgsStr);
    iArg++;
  }

   /* d) Convert char **, an array of character arrays*/
  if ( nStrRea > 0 ){
    pArgsStr = PyList_New(nStrRea);
    
    for (i = 0; i < nStrRea; ++i) {
      /* Convert argument to a python float*/
      /*      Py_ssize_t len = 0;*/
      /* According to the Modelica Specification, strings are terminated by '\0'*/
      /* Seek the string length*/
      /*      while (strRea[i][len] != '\0')*/
      /*	len++;*/
      
      /*      pValue = PyUnicode_FromStringAndSize(strRea[i], len);*/
      pValue =  PyUnicode_FromString(strRea[i]);
      if (!pValue) {
	/* Failed to convert argument.*/
	Py_DECREF(pArgsStr);
	Py_DECREF(pModule);
	/* According to the Modelica specification, */
	/* the function ModelicaError never returns to the calling function.*/
	(*ModelicaFormatError)("Cannot convert string argument number %i to Python format.", i);
      }
      /* pValue reference stolen here*/
      PyList_SetItem(pArgsStr, i, pValue);
    }
    /* If there is only a scalar string, then don't build a list.*/
    /* Just put the scalar value into the list of arguments.*/
    if ( nStrRea == 1)
	PyTuple_SetItem(pArgs, iArg, PyList_GetItem(pArgsStr, (Py_ssize_t)0));
      else
	PyTuple_SetItem(pArgs, iArg, pArgsStr);
    iArg++;
  }

  /* Convert the arguments*/
  /* e) Convert double[]*/
  if (nDblParWri > 0){
	  pArgsDbl = PyList_New(nDblParWri);
	  for (i = 0; i < nDblParWri; ++i) {
		  /* Convert argument to a python float*/
		  pValue = PyFloat_FromDouble(dblValParWri[i]);
		  if (!pValue) {
			  /* Failed to convert argument.*/
			  Py_DECREF(pArgsDbl);
			  Py_DECREF(pModule);
			  /* According to the Modelica specification,*/
			  /* the function ModelicaError never returns to the calling function.*/
			  (*ModelicaFormatError)("Cannot convert double argument number %i to Python format.", i);
		  }
		  /* pValue reference stolen here*/
		  PyList_SetItem(pArgsDbl, i, pValue);
	  }
	  /* If there is only a scalar double, then don't build a list.*/
	  /* Just put the scalar value into the list of arguments*/
	  if (nDblParWri == 1)
		  PyTuple_SetItem(pArgs, iArg, PyList_GetItem(pArgsDbl, (Py_ssize_t)0));
	  else
		  PyTuple_SetItem(pArgs, iArg, pArgsDbl);
	  iArg++;
  }

  /* f) Convert char **, an array of character arrays*/
  if (nStrParWri > 0){
	  pArgsStr = PyList_New(nStrParWri);

	  for (i = 0; i < nStrParWri; ++i) {
		  /* Convert argument to a python float*/
		  /*      Py_ssize_t len = 0;*/
		  /* According to the Modelica Specification, strings are terminated by '\0'*/
		  /* Seek the string length*/
		  /*      while (strParWri[i][len] != '\0')*/
		  /*	len++;*/

		  /*      pValue = PyUnicode_FromStringAndSize(strParWri[i], len);*/
		  pValue = PyUnicode_FromString(strParWri[i]);
		  if (!pValue) {
			  /* Failed to convert argument.*/
			  Py_DECREF(pArgsStr);
			  Py_DECREF(pModule);
			  /* According to the Modelica specification,*/
			  /* the function ModelicaError never returns to the calling function.*/
			  (*ModelicaFormatError)("Cannot convert string argument number %i to Python format.", i);
		  }
		  /* pValue reference stolen here*/
		  PyList_SetItem(pArgsStr, i, pValue);
	  }
	  /* If there is only a scalar string, then don't build a list.*/
	  /* Just put the scalar value into the list of arguments.*/
	  if (nStrParWri == 1)
		  PyTuple_SetItem(pArgs, iArg, PyList_GetItem(pArgsStr, (Py_ssize_t)0));
	  else
		  PyTuple_SetItem(pArgs, iArg, pArgsStr);
	  iArg++;
  }

  /* Convert the arguments*/
  /* g) Convert double[]*/
  pArgsDbl = PyList_New(1);
  /* Convert argument to a python float*/
  pValue = PyFloat_FromDouble(resWri[0]);
  if (!pValue) {
	  /* Failed to convert argument.*/
	  Py_DECREF(pArgsDbl);
	  Py_DECREF(pModule);
	  /* According to the Modelica specification,*/
	  /* the function ModelicaError never returns to the calling function.*/
	  (*ModelicaFormatError)("Cannot convert double argument %f for result writing to Python format.", resWri[0]);
  }
  /* pValue reference stolen here*/
  PyList_SetItem(pArgsDbl, 0, pValue);
  /* If there is only a scalar double, then don't build a list.*/
  /* Just put the scalar value into the list of arguments*/
  PyTuple_SetItem(pArgs, iArg, PyList_GetItem(pArgsDbl, (Py_ssize_t)0));
  iArg++;
  
  /*//////////////////////////////////////////////////////////////////////////*/
  /*//////////////////////////////////////////////////////////////////////////*/
  /* Call the Python function*/
  pValue = PyObject_CallObject(pFunc, pArgs);
  if (pArgs != NULL)
    Py_DECREF(pArgs);

  /*//////////////////////////////////////////////////////////////////////////*/
  /* Check whether the call to the Python function failed.*/
  if (pValue == NULL) {

    /*    PyErr_Print();*/
    PyObject *pValue, *pType, *pTraceBack;
    PyErr_Fetch(&pType, &pValue, &pTraceBack);
    if (pType != NULL)
      Py_DECREF(pType);
    if (pTraceBack != NULL)
      Py_DECREF(pTraceBack);
    Py_DECREF(pFunc);
    Py_DECREF(pModule);
    /* Py_Finalize(); // removed, see note at other Py_Finalize() statement*/
    (*ModelicaFormatError)("Call to Python function failed.\n \
This is often due to an error in the Python script,\n \
or because the list of arguments of the Python function is incorrect.\n \
Check the module \"%s\".\n \
The error message is \"%s\"",
                        moduleName,
                        PyBytes_AsString(PyObject_Repr(pValue)));
  }

  /*//////////////////////////////////////////////////////////////////////////*/
  /* Set up the variables that indicate the return data types of the function*/
  if ( nDblRea > 0)
    nRet++;

  /* Check whether the function must returns some values*/
  if (nRet > 0){
    /*//////////////////////////////////////////////////////////////////////////*/
    /* The function returned some arguments.*/
    /* If there are multiple return values, then it must be a list*/
    if (nRet > 1){
      /* Check whether it is a list*/
      if (!PyList_Check(pValue)){
	(*ModelicaFormatError)("Python function \"%s\" does not return a list.\n\
The returned object is \"%s\"",
			    functionName, PyBytes_AsString(PyObject_Repr(pValue)));
      }
    }
    /* Check whether the list has the right number of arguments.*/
    /* If nRet==2, then it must be a list with two values. If nRet > 2, it may*/
    /* be a list with three values, or a two lists, one with one and one with two values.*/
    /* Hence, we only check for nRet==2.*/
    if ( nRet == 2){
      if ( nRet != PyList_Size(pValue) ){
	(*ModelicaFormatError)("Python function \"%s\", returns a list with %i elements,\n \
but expected two elements.\n\
The returned object is \"%s\"",
			    functionName,
			    PyList_Size(pValue),
			    PyBytes_AsString(PyObject_Repr(pValue)));
      }
    }
	/*//////////////////////////////////////////////////////////////////////////*/
	/* Parse double values, if we have some*/
	if (nDblRea > 0){
		/* Check if the function only returns double values*/
		if (nRet == 1)
			pItemDbl = pValue;
		else{
			pItemDbl = PyList_GetItem(pValue, iRet);
			iRet++;
		}
		/* Check the number of return arguments*/
		if (nDblRea > 1 && nDblRea != PyList_Size(pItemDbl))
			(*ModelicaFormatError)("For Python function \"%s\", Modelica declares that Python returns %i doubles,\
								    but Python returned %i values.\n\
									The returned object is \"%s\"",
									functionName, nDblRea, PyList_Size(pItemDbl),
									PyBytes_AsString(PyObject_Repr(pValue)));

		/* The number of arguments is correct. Retrieve them and parse them.*/
		/* If nDblRea == 1, then it is a scalar, else it is a list*/
		if (nDblRea == 1){
			/* Check whether it is a float or an integer.*/
			/* (For integers, PyFloat_Check(p) returns false, hence we also call PyLong_Check(p))*/
			if (PyFloat_Check(pItemDbl) || PyLong_Check(pItemDbl) || PyLong_Check(pItemDbl))
				dblValRea[0] = PyFloat_AsDouble(pItemDbl);
			else
				(*ModelicaFormatError)("Python function \"%s\" returns an invalid object for a scalar double value.\n\
									   There should only be one double value returned.\n\
									   The returned object is \"%s\".",
									   functionName, PyBytes_AsString(PyObject_Repr(pValue)));
		}
		else{ /* We have nDblRea > 1, iterate through the list*/
			for (pIndVal = 0; pIndVal < PyList_Size(pItemDbl); ++pIndVal){
				PyObject *p = PyList_GetItem(pItemDbl, pIndVal);
				/* Check whether it is a float or an integer.*/
				/* (For integers, PyFloat_Check(p) returns false, hence we also call PyLong_Check(p))*/
				if (PyFloat_Check(p) || PyLong_Check(p) || PyLong_Check(p))
					dblValRea[pIndVal] = PyFloat_AsDouble(p);
				else
					(*ModelicaFormatError)("Python function \"%s\" returns an invalid object for a scalar double value.\n\
										   The returned object is \"%s\".",
										   functionName, PyBytes_AsString(PyObject_Repr(pValue)));
			} /* for(...)*/
		}
	}/* nDblRea > 0*/
	else{
		/* Modelica has no arrays with zero lenght. Hence, dblValRea has size 1 if nDblRea = 0.*/
		/* Assign a zero value to this element.*/
		dblValRea[0] = 0;
	}

  } /* end of if (nRet > 0)*/

  /*//////////////////////////////////////////////////////////////////////////*/
  /* Decrement the reference counters*/
  /* causes sometimes a segmentation fault    Py_DECREF(pValue);*/
  /* causes sometimes a segmentation fault    Py_DECREF(pFunc);*/
  /* causes sometimes a segmentation fault    Py_DECREF(pModule);*/
  /* causes sometimes a segmentation fault    Py_DECREF(pModule);*/
  /* Undo all initializations*/
  /* We uncommented Py_Finalize() because it caused a segmentation fault on Ubuntu 12.04 32 bit.*/
  /* The segmentation fault was randomly produced by the statement, and often observed when running*/
  /* simulateModel("CYMDISTToFMU.Utilities.IO.Python27.Functions.Examples.TestPythonInterface");*/
  /**/
  /* See also the discussion at*/
  /* http://stackoverflow.com/questions/7676314/py-initialize-py-finalize-not-working-twice-with-numpy*/
  /**/
  /*  Py_Finalize();*/

  return;
}

/*
// 3/26/2013- TN: checkStringLength is commented out since it is not used.
void checkStringLength(const char * str, size_t strLen){
  int i;
  int n;

  n = -1;
  for(i = 0; i < strLen+1; i++){
    if (str[i] == '\0'){
      n = i;
      break;
    }
  }
  if (n == -1)
    //    ModelicaFormatError("String %.2s has more than %d characters. Increase parameter strLen.",
    ModelicaFormatError("String %s has more than %d characters. Increase parameter strLen.",
                        str, strLen);
  return;
}
*/
