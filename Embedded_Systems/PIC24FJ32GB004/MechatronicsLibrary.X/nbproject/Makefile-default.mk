#
# Generated Makefile - do not edit!
#
# Edit the Makefile in the project folder instead (../Makefile). Each target
# has a -pre and a -post target defined where you can add customized code.
#
# This makefile implements configuration specific macros and targets.


# Include project Makefile
ifeq "${IGNORE_LOCAL}" "TRUE"
# do not include local makefile. User is passing all local related variables already
else
include Makefile
# Include makefile containing local settings
ifeq "$(wildcard nbproject/Makefile-local-default.mk)" "nbproject/Makefile-local-default.mk"
include nbproject/Makefile-local-default.mk
endif
endif

# Environment
MKDIR=gnumkdir -p
RM=rm -f 
MV=mv 
CP=cp 

# Macros
CND_CONF=default
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
IMAGE_TYPE=debug
OUTPUT_SUFFIX=a
DEBUGGABLE_SUFFIX=a
FINAL_IMAGE=dist/${CND_CONF}/${IMAGE_TYPE}/MechatronicsLibrary.X.${OUTPUT_SUFFIX}
else
IMAGE_TYPE=production
OUTPUT_SUFFIX=a
DEBUGGABLE_SUFFIX=a
FINAL_IMAGE=dist/${CND_CONF}/${IMAGE_TYPE}/MechatronicsLibrary.X.${OUTPUT_SUFFIX}
endif

# Object Directory
OBJECTDIR=build/${CND_CONF}/${IMAGE_TYPE}

# Distribution Directory
DISTDIR=dist/${CND_CONF}/${IMAGE_TYPE}

# Source Files Quoted if spaced
SOURCEFILES_QUOTED_IF_SPACED=src/circularBuffer.c src/crc.c

# Object Files Quoted if spaced
OBJECTFILES_QUOTED_IF_SPACED=${OBJECTDIR}/src/circularBuffer.o ${OBJECTDIR}/src/crc.o
POSSIBLE_DEPFILES=${OBJECTDIR}/src/circularBuffer.o.d ${OBJECTDIR}/src/crc.o.d

# Object Files
OBJECTFILES=${OBJECTDIR}/src/circularBuffer.o ${OBJECTDIR}/src/crc.o

# Source Files
SOURCEFILES=src/circularBuffer.c src/crc.c


CFLAGS=
ASFLAGS=
LDLIBSOPTIONS=

############# Tool locations ##########################################
# If you copy a project from one host to another, the path where the  #
# compiler is installed may be different.                             #
# If you open this project with MPLAB X in the new host, this         #
# makefile will be regenerated and the paths will be corrected.       #
#######################################################################
# fixDeps replaces a bunch of sed/cat/printf statements that slow down the build
FIXDEPS=fixDeps

.build-conf:  ${BUILD_SUBPROJECTS}
ifneq ($(INFORMATION_MESSAGE), )
	@echo $(INFORMATION_MESSAGE)
endif
	${MAKE}  -f nbproject/Makefile-default.mk dist/${CND_CONF}/${IMAGE_TYPE}/MechatronicsLibrary.X.${OUTPUT_SUFFIX}

MP_PROCESSOR_OPTION=24FJ32GB004
MP_LINKER_FILE_OPTION=,--script=p24FJ32GB004.gld
# ------------------------------------------------------------------------------------
# Rules for buildStep: compile
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
${OBJECTDIR}/src/circularBuffer.o: src/circularBuffer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/circularBuffer.o.d 
	@${RM} ${OBJECTDIR}/src/circularBuffer.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  src/circularBuffer.c  -o ${OBJECTDIR}/src/circularBuffer.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/src/circularBuffer.o.d"      -g -D__DEBUG -D__MPLAB_DEBUGGER_PK3=1    -omf=elf -O0 -msmart-io=1 -Wall -msfr-warn=off
	@${FIXDEPS} "${OBJECTDIR}/src/circularBuffer.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/src/crc.o: src/crc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/crc.o.d 
	@${RM} ${OBJECTDIR}/src/crc.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  src/crc.c  -o ${OBJECTDIR}/src/crc.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/src/crc.o.d"      -g -D__DEBUG -D__MPLAB_DEBUGGER_PK3=1    -omf=elf -O0 -msmart-io=1 -Wall -msfr-warn=off
	@${FIXDEPS} "${OBJECTDIR}/src/crc.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
else
${OBJECTDIR}/src/circularBuffer.o: src/circularBuffer.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/circularBuffer.o.d 
	@${RM} ${OBJECTDIR}/src/circularBuffer.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  src/circularBuffer.c  -o ${OBJECTDIR}/src/circularBuffer.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/src/circularBuffer.o.d"        -g -omf=elf -O0 -msmart-io=1 -Wall -msfr-warn=off
	@${FIXDEPS} "${OBJECTDIR}/src/circularBuffer.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
${OBJECTDIR}/src/crc.o: src/crc.c  nbproject/Makefile-${CND_CONF}.mk
	@${MKDIR} "${OBJECTDIR}/src" 
	@${RM} ${OBJECTDIR}/src/crc.o.d 
	@${RM} ${OBJECTDIR}/src/crc.o 
	${MP_CC} $(MP_EXTRA_CC_PRE)  src/crc.c  -o ${OBJECTDIR}/src/crc.o  -c -mcpu=$(MP_PROCESSOR_OPTION)  -MMD -MF "${OBJECTDIR}/src/crc.o.d"        -g -omf=elf -O0 -msmart-io=1 -Wall -msfr-warn=off
	@${FIXDEPS} "${OBJECTDIR}/src/crc.o.d" $(SILENT)  -rsi ${MP_CC_DIR}../ 
	
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: assemble
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: assemblePreproc
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
else
endif

# ------------------------------------------------------------------------------------
# Rules for buildStep: archive
ifeq ($(TYPE_IMAGE), DEBUG_RUN)
dist/${CND_CONF}/${IMAGE_TYPE}/MechatronicsLibrary.X.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk    
	@${MKDIR} dist/${CND_CONF}/${IMAGE_TYPE} 
	@${RM} dist/${CND_CONF}/${IMAGE_TYPE}/MechatronicsLibrary.X.${OUTPUT_SUFFIX} 
	${MP_AR} $(MP_EXTRA_AR_PRE)  -omf=elf -r dist/${CND_CONF}/${IMAGE_TYPE}/MechatronicsLibrary.X.${OUTPUT_SUFFIX}  ${OBJECTFILES_QUOTED_IF_SPACED}      
	
else
dist/${CND_CONF}/${IMAGE_TYPE}/MechatronicsLibrary.X.${OUTPUT_SUFFIX}: ${OBJECTFILES}  nbproject/Makefile-${CND_CONF}.mk   
	@${MKDIR} dist/${CND_CONF}/${IMAGE_TYPE} 
	@${RM} dist/${CND_CONF}/${IMAGE_TYPE}/MechatronicsLibrary.X.${OUTPUT_SUFFIX} 
	${MP_AR} $(MP_EXTRA_AR_PRE)  -omf=elf -r dist/${CND_CONF}/${IMAGE_TYPE}/MechatronicsLibrary.X.${OUTPUT_SUFFIX}  ${OBJECTFILES_QUOTED_IF_SPACED}      
	
endif


# Subprojects
.build-subprojects:


# Subprojects
.clean-subprojects:

# Clean Targets
.clean-conf: ${CLEAN_SUBPROJECTS}
	${RM} -r build/default
	${RM} -r dist/default

# Enable dependency checking
.dep.inc: .depcheck-impl

DEPFILES=$(shell mplabwildcard ${POSSIBLE_DEPFILES})
ifneq (${DEPFILES},)
include ${DEPFILES}
endif
