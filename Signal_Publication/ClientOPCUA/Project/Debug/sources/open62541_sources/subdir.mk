################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/home/chris/CRT/ClientOPCUA/sources/open62541_sources/open62541.c 

C_DEPS += \
./sources/open62541_sources/open62541.d 

OBJS += \
./sources/open62541_sources/open62541.o 


# Each subdirectory must supply rules for building sources it contributes
sources/open62541_sources/open62541.o: /home/chris/CRT/ClientOPCUA/sources/open62541_sources/open62541.c sources/open62541_sources/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


clean: clean-sources-2f-open62541_sources

clean-sources-2f-open62541_sources:
	-$(RM) ./sources/open62541_sources/open62541.d ./sources/open62541_sources/open62541.o

.PHONY: clean-sources-2f-open62541_sources

