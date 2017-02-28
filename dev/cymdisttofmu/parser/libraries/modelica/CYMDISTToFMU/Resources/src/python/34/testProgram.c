#include "testProgram.h"

void ModelicaFormatError(const char* string, const char* fmt, const char* val){
  fprintf(stderr, string, fmt, val);
  fprintf(stderr, "\n");
  exit(1);
}

int main(int nArgs, char ** args){
	
  /* Parameters for testing cymdist interface*/
  const char * moduleName="testCymdist";
  const char * functionName="r1_r1";
  const char * configFileName="config.csv";
  double time[]={0.0};
  
  size_t nDblWri=1;
  double dblValWri[]={15.0};
  const char *strWri[]={"u"};
  
  size_t nDblRea=1;
  double dblValRea[1];
  const char *strRea[]={"y"};
  
  size_t nDblParWri=0;
  const char * strParWri[]={""};
  int dblValParWri[]={0};
  double resWri[]={0};

  int i;
  
    for(i=0; i < 10; i++){
    printf("Calling with i for cymdist = %d.\n", i);
    pythonExchangeValuesCymdistNoModelica(moduleName,
                          functionName, 
						  configFileName, 
						  time,
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
						  ModelicaFormatError);
	}

  return 0;
}

