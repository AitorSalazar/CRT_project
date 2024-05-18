################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
/home/chris/CRT/ClientOPCUA/sources/ClientOPCUA.c 

C_DEPS += \
./sources/ClientOPCUA.d 

OBJS += \
./sources/ClientOPCUA.o 


# Each subdirectory must supply rules for building sources it contributes
sources/ClientOPCUA.o: /home/chris/CRT/ClientOPCUA/sources/ClientOPCUA.c sources/subdir.mk
	@echo 'Building file: $<'
	@echo 'Invoking: GCC C Compiler'
	gcc -O0 -g3 -Wall -c -fmessage-length=0 -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


clean: clean-sources

clean-sources:
	-$(RM) ./sources/ClientOPCUA.d ./sources/ClientOPCUA.o

.PHONY: clean-sources

