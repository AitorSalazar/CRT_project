/*
 * OpcUaServer.c
 *
 *  Created on: 9 may 2024
 *      Author: Christopher.Carmona and Aitor Salazar
 */

#include "open62541.h"
#include <signal.h>
#include <stdlib.h>

#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <string.h>
#include <pthread.h>


//############################## Constants #######################################
#define HUMIDITY_NODE_NAME 	"Humidity"
#define TEMP_NODE_NAME 		"Temperature"

#define MEMORY_SIZE 		2048
#define MEMORY_NAME 		"/shm_temp_humidity"

//############################### DataTypes ######################################
typedef struct{
	int	 	humidity;
	float  	temp;
}st_SensorData;

typedef struct
{
	st_SensorData 	*pSensordata;	// [out]Data from Sensor 
	void 			*ptr; 			// [in] Shared memory physical address First 12 bytes (3* 4 bytes) are needed data
}st_dataForUpdateThread;

//############################### Global Variables	###############################
static volatile UA_Boolean running = true;

//############################### Functions	###############################
static void stopHandler(int sig)
{
    UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND, "received ctrl-c");
    running = false;
}



UA_StatusCode readValue(UA_Server *server,
		               const UA_NodeId *sessionId, void *sessionContext,
					   const UA_NodeId *nodeId, void *nodeContext,
					   UA_Boolean sourceTimeStamp, const UA_NumericRange *range,
					   UA_DataValue *dataValue)
{
	st_SensorData *pDataToShow = (st_SensorData *)nodeContext;

	if (!strcmp((char *)nodeId->identifier.string.data, HUMIDITY_NODE_NAME))
	{
		UA_Variant_setScalarCopy(&dataValue->value, &pDataToShow->humidity,&UA_TYPES[UA_TYPES_INT32]);
	}
	else if (!strcmp((char *)nodeId->identifier.string.data, TEMP_NODE_NAME))
	{
		UA_Variant_setScalarCopy(&dataValue->value, &pDataToShow->temp,&UA_TYPES[UA_TYPES_FLOAT]);
	}
	else
	{
		return 1;
	}
	dataValue->hasValue = true;
	return UA_STATUSCODE_GOOD;
}

UA_StatusCode writeValue(UA_Server *server,
						 const UA_NodeId *sessionId, void *sessionContext,
						 const UA_NodeId *nodeId, void *nodeContext,
						 const UA_NumericRange *range, const UA_DataValue *data)
{
	UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
				"This value can not be changed");
	return UA_STATUSCODE_BADINTERNALERROR;
}

UA_StatusCode addValueMonitoredItem(	UA_Server *pServer,
											char* nodeName,
											UA_NodeId type,
											UA_Byte accessLevel,
											st_SensorData *pSensorData)
{
	UA_StatusCode 			retval = UA_STATUSCODE_GOOD ;
	UA_VariableAttributes 	attr;
	UA_NodeId 				ValueNodeId;
	UA_NodeId 				parentNodeId;
	UA_NodeId 				parentReferenceNodeId;
	UA_NodeId 				variableTypeNodeId;
	UA_QualifiedName 		ValueQName;
	UA_DataSource 			ValueDataSource;

	//Rellenar atributos del nodo
	attr = UA_VariableAttributes_default;

	attr.description 		= UA_LOCALIZEDTEXT("en-US",nodeName);
	attr.displayName 		= UA_LOCALIZEDTEXT("en-US",nodeName);
	attr.dataType = type;

	attr.accessLevel = accessLevel;
	if (!strcmp(nodeName, HUMIDITY_NODE_NAME))
	{
		UA_Variant_setScalarCopy(&attr.value, (UA_Int32 *)&pSensorData->humidity, &UA_TYPES[UA_TYPES_INT32]);
	}
	else if (!strcmp(nodeName, TEMP_NODE_NAME))
	{

		UA_Variant_setScalarCopy(&attr.value,(UA_Float *)&pSensorData->temp,&UA_TYPES[UA_TYPES_FLOAT]);
	}

	ValueNodeId 			= UA_NODEID_STRING(1, nodeName);
	ValueQName				= UA_QUALIFIEDNAME(1, nodeName);
	parentNodeId 			= UA_NODEID_NUMERIC(0, UA_NS0ID_OBJECTSFOLDER);
	parentReferenceNodeId 	= UA_NODEID_NUMERIC(0, UA_NS0ID_ORGANIZES);
	variableTypeNodeId 		= UA_NODEID_NUMERIC(0, UA_NS0ID_BASEDATAVARIABLETYPE);

	//asignar funciones de lectura y escritura del DataSource
	ValueDataSource.read = readValue;
	ValueDataSource.write = writeValue;

	retval= UA_Server_addDataSourceVariableNode(	pServer,
													ValueNodeId,
													parentNodeId,
													parentReferenceNodeId,
													ValueQName,
													variableTypeNodeId,
													attr,
													ValueDataSource,
													(void*)pSensorData, //Por aqui se pasa el puntero del dato
//													NULL,
													NULL);
	return retval;
}


UA_StatusCode addVariableHumidity(UA_Server *pServer)
{

	UA_StatusCode retval = UA_STATUSCODE_GOOD;
	/* Define the attribute of the myInteger variable node */
	UA_VariableAttributes attr = UA_VariableAttributes_default;
	UA_Int32 i4Humidity = 1;
	UA_Variant_setScalar(&attr.value, &i4Humidity, &UA_TYPES[UA_TYPES_INT32]);
	attr.description = UA_LOCALIZEDTEXT("en-US","Humidity value in %");
	attr.displayName = UA_LOCALIZEDTEXT("en-US","Humidity");
	attr.dataType = UA_TYPES[UA_TYPES_INT32].typeId;
	attr.accessLevel = UA_ACCESSLEVELMASK_READ;

	/* Add the variable node to the information model */
	UA_NodeId humidityNodeId = UA_NODEID_STRING(1, "humidityNodeId");
	UA_QualifiedName humidityName = UA_QUALIFIEDNAME(1, "humidity");
	UA_NodeId parentNodeId = UA_NODEID_NUMERIC(0, UA_NS0ID_OBJECTSFOLDER);
	UA_NodeId parentReferenceNodeId = UA_NODEID_NUMERIC(0, UA_NS0ID_ORGANIZES);
	retval= UA_Server_addVariableNode(	pServer,
										humidityNodeId,
										parentNodeId,
										parentReferenceNodeId,
										humidityName,
										UA_NODEID_NUMERIC(0, UA_NS0ID_BASEDATAVARIABLETYPE),
										attr,
										NULL,
										NULL);
	return retval;
}
UA_StatusCode buildDataModel(UA_Server *pServer, st_SensorData *pSensorData)
{
	UA_StatusCode retval = UA_STATUSCODE_GOOD;

	retval = addValueMonitoredItem(	pServer,
											HUMIDITY_NODE_NAME,
											UA_TYPES[UA_TYPES_INT32].typeId,
											UA_ACCESSLEVELMASK_READ,
											pSensorData
											);
	if (retval== UA_STATUSCODE_GOOD)
	{
	UA_LOG_INFO(UA_Log_Stdout,UA_LOGCATEGORY_SESSION,
				"Added Humidity node to Data Model");
	}
	else
	{
		return retval;
	}
	retval = addValueMonitoredItem(	pServer,
											TEMP_NODE_NAME,
											UA_TYPES[UA_TYPES_FLOAT].typeId,
											UA_ACCESSLEVELMASK_READ,
											pSensorData
											);
	if (retval== UA_STATUSCODE_GOOD)
	{
	UA_LOG_INFO(UA_Log_Stdout,UA_LOGCATEGORY_SESSION,
				"Added Temperature node to Data Model");
	}
	else
	{
		UA_LOG_ERROR(UA_Log_Stdout,UA_LOGCATEGORY_SESSION,
						"Error Adding Temperature node to Data Model \n Error is %s",UA_StatusCode_name(retval));
		return retval;
	}

	return retval;

}


void * UpdateData(void *dataForUpdateThread)
{
	st_dataForUpdateThread *pDataForUpdateThread = (st_dataForUpdateThread *)dataForUpdateThread;
	int 	temp_int;
	int 	temp_frac;
	float 	aux_temperature;
	int 	*pMemory=(int *)pDataForUpdateThread->ptr;
	do {
		pDataForUpdateThread->pSensordata->humidity = *pMemory;
		temp_int =pMemory[1];
		temp_frac = pMemory[2];
		aux_temperature = temp_int + (float)temp_frac/100.0f;
		pDataForUpdateThread->pSensordata->temp = aux_temperature;
		printf("current values are hum: %i temp: %f\n",pDataForUpdateThread->pSensordata->humidity,pDataForUpdateThread->pSensordata->temp);
		usleep(100000);

	 }while(true);


}

int configurateServer (UA_Server *pServer) 
{
	UA_StatusCode 		retval;
	UA_String 			urlAddress[1];
	UA_ServerConfig 	*pConfig = UA_Server_getConfig(pServer);
    char 				ipAddress[]= "opc.tcp://Raspi4Chris.local:4840";

	urlAddress[0]= UA_STRING(ipAddress);
	retval = UA_Array_copy(urlAddress,1, (void *) &pConfig->serverUrls,&UA_TYPES[UA_TYPES_STRING]);
	pConfig->serverUrlsSize = 1;
	return (int)retval;
}


void allocateSharedMem(int *pshm_fd,void **ptr)
{	
	int TryCounter = 0;
	*pshm_fd=-1;
	while (*pshm_fd<0){

	*pshm_fd = shm_open(MEMORY_NAME, O_RDONLY, 0666);
    if (*pshm_fd == -1) {
		if (TryCounter == 10){

			perror("shm_open");
			exit(EXIT_FAILURE);
		}
		TryCounter++;
		printf("%i. Trying to connect to shared memory\n",TryCounter);
		sleep(1);
    }
	}

    // Map the shared memory object into process address space
    *ptr = mmap(NULL, MEMORY_SIZE, PROT_READ, MAP_SHARED, *pshm_fd, 0);
    if (ptr == MAP_FAILED) {
        perror("mmap");
        exit(EXIT_FAILURE);
    }
}

void freeSharedMem(int *pshm_fd,void**ptr)
{
	 // Unmap the shared memory
    if (munmap(*ptr, MEMORY_SIZE) == -1) {
        perror("munmap");
        exit(EXIT_FAILURE);
    }

    // Close the shared memory object
    if (close(*pshm_fd) == -1) {
        perror("close");
        exit(EXIT_FAILURE);
    }
}

int main(void) {
    signal(SIGINT, stopHandler);
    signal(SIGTERM, stopHandler);

	int 					shm_fd;
	void					*ptr;
    UA_StatusCode 			retval;
    st_SensorData 			sensorData = {.temp = 0.0,.humidity = 0};
    st_dataForUpdateThread 	dataForUpdateThread;
	pthread_t 				id;
    UA_Server 				*pServer;

	pServer = UA_Server_new();
	configurateServer(pServer);
	//Data model for this task
	retval = buildDataModel(pServer,&sensorData);
	allocateSharedMem(&shm_fd,&ptr);

	//Run thread to make polling to shared memory
	dataForUpdateThread.pSensordata = &sensorData;
	dataForUpdateThread.ptr = ptr;
	pthread_create(&id, NULL, &UpdateData, (void *)&dataForUpdateThread); 
	
	// Run the server
	retval = UA_Server_runUntilInterrupt(pServer);

	freeSharedMem(&shm_fd,ptr);

	//Clean the server from memory
    UA_Server_delete(pServer);
    return retval == UA_STATUSCODE_GOOD ? EXIT_SUCCESS : EXIT_FAILURE;
}