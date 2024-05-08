
#include "open62541.h"
bool running = true;

int main()
{
    UA_StatusCode Status= UA_STATUSCODE_GOOD;

    UA_Server *pServer = UA_Server_new();
    //UA_Server_run(pServer,(UA_Boolean *)&running);
    Status = UA_Server_runUntilInterrupt(pServer);
    //Cleanup
    UA_Server_delete(pServer);

    return Status;

}