
/* Exchange values with Cymdist.*/
/* Any argument that starts with 'n', such as nDblWri, may be zero.*/
/* If there is an error, then this function calls*/
/* ModelicaFormatError(...) which terminates the computation.*/
/**/
/* The arguments are as follows:*/
/*  moduleName            - Name of the Python module.*/
/*  functionName          - Name of the Python function.*/
/*  modNamRef             - Double value which references a CYMDIST model.*/
/*  nDblWri               - Number of inputs values to write.*/
/*  strWri                - Name of inputs to write.*/
/*  dblValWri             - Double inputs values to write.*/
/*  nDblRea               - Number of outputs values to read.*/
/*  strRea                - Name of outputs to read.*/
/*  dblValRea             - Double outputs values to read.*/
/*  nDblParWri            - Number of parameters to write.*/
/*  strParWri             - Name of parameters to write.*/
/*  dblValParWri          - Double values of parameters to write.*/
/*  resWri                - Double value to indicate if results should be written.*//
#include <ModelicaUtilities.h>

void pythonExchangeValuesCymdist(const char * moduleName,
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
							double * resWri,)
{
  pythonExchangeValuesCymdistNoModelica(
   moduleName,
   functionName,
   modNamRef,
   nDblWri, 
   strWri,
   dblValWri, 
   nDblRea,
   strRea, 
   dblValRea,
   nDblParWri, 
   strParWri,
   dblValParWri, 
   resWri,
   ModelicaFormatError
  );
}

