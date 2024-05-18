/*
 * ClientOPCUA.c
 *
 *  Created on: 14 Apr 2024
 *      Author: chris
 */

#include "open62541_sources/open62541.h"
#include <unistd.h>
#include <signal.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>

bool running = true;

#define MEMORY_SIZE 		2048
#define MEMORY_NAME 		"/shm_temp_humidity"

static void stopHandler(int sig)
{
    UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND, "received ctrl-c");
    running = false;
}

void allocateSharedMem(int *pshm_fd,void **ptr)
{	
	int TryCounter = 0;
	*pshm_fd=-1;
	while (*pshm_fd<0)
    {
        *pshm_fd = shm_open(MEMORY_NAME, O_RDWR, 0666);
        if (*pshm_fd == -1) 
        {
            if (TryCounter == 10)
            {  

                perror("shm_open");
                exit(EXIT_FAILURE);
            }
            TryCounter++;
            printf("%i. Trying to connect to shared memory\n",TryCounter);
            sleep(1);
        }
	}

    // Map the shared memory object into process address space
    *ptr = mmap(NULL, MEMORY_SIZE, PROT_READ | PROT_WRITE, MAP_SHARED, *pshm_fd, 0);
    if (*ptr == MAP_FAILED) {
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

int main(void) 
{
    signal(SIGINT, stopHandler);
    signal(SIGTERM, stopHandler);

    int             TryCounter=0;
    bool            connected = false;
    int 		    shm_fd;
	void		    *ptr;
    UA_StatusCode   retval;
    UA_Variant      valueTemp; 
    UA_Variant      valueHum; 
    UA_Float        raw_Temp;
    UA_Int32        raw_Hum;
    UA_NodeId       nodeIdHum;
    UA_NodeId       nodeIdTemp;
    
    UA_Client *client = UA_Client_new();
    UA_ClientConfig_setDefault(UA_Client_getConfig(client));
    
    allocateSharedMem(&shm_fd,&ptr);
    
    while(!connected)
    {
   	    retval = UA_Client_connect(client, "opc.tcp://Raspi4Chris.local:4840");
    	if(retval != UA_STATUSCODE_GOOD)
        {
            UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                	    "The connection failed with status code %s",
                   			 UA_StatusCode_name(retval));
        
            printf("%i Try to connect to Server\n",TryCounter);
            sleep(1);
        }
        else 
        {
            connected= true;
        }

        if (TryCounter == 10 )
        {
            break;
        }
    }
    
    if(!connected)
    {
        freeSharedMem(&shm_fd,ptr);
        UA_Client_delete(client);
   	    return 0;
    }


    /* Read the value attribute of the node. UA_Client_readValueAttribute is a
     * wrapper for the raw read service available as UA_Client_Service_read. */
    UA_Variant_init(&valueTemp);
    UA_Variant_init(&valueHum);

    /* NodeId of the variable holding the current time */
    nodeIdHum = UA_NODEID_STRING(1,"Humidity");
    nodeIdTemp = UA_NODEID_STRING(1,"Temperature");
    
    int * intptr = (int *)ptr;
    float auxfloat;
    while (running)
    {
        retval = UA_Client_readValueAttribute(client, nodeIdHum, &valueHum);
        retval = UA_Client_readValueAttribute(client, nodeIdTemp, &valueTemp);

        if(retval == UA_STATUSCODE_GOOD && UA_Variant_hasScalarType(&valueTemp, &UA_TYPES[UA_TYPES_FLOAT])) {
            raw_Temp = *(UA_Float *) valueTemp.data;
            intptr[1] = (int)raw_Temp;
            auxfloat = (((float)raw_Temp) * 100.0)-100*((int)raw_Temp);
            intptr[2] = (int)(auxfloat);
            UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                        "Temperature is: %f",
                        raw_Temp);
        } 
        else 
        {
            UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                        "Reading the value failed with status code %s",
                        UA_StatusCode_name(retval));
        }
        if(retval == UA_STATUSCODE_GOOD && UA_Variant_hasScalarType(&valueHum, &UA_TYPES[UA_TYPES_INT32])) {
            raw_Hum = *(UA_Int32 *) valueHum.data;
            printf("raw_Hum: %i\n",(int)raw_Hum);
            intptr[0] = (int)raw_Hum;
            UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,git
                        "Humidity is: %i",
                        raw_Hum);
        } else {
            UA_LOG_INFO(UA_Log_Stdout, UA_LOGCATEGORY_USERLAND,
                        "Reading the value failed with status code %s",
                        UA_StatusCode_name(retval));
        }
        usleep(200000);
    }

    /* Clean up */
    UA_Variant_clear(&valueHum);
    UA_Variant_clear(&valueTemp);
    UA_Client_delete(client); /* Disconnects the client internally */
    freeSharedMem(&shm_fd,&ptr);
    return 0;
}


