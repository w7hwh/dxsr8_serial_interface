######################################################################
#  Project Makefile
######################################################################

BINARY		= dxsr8_interface

SRCFILES	= dxsr8_interface.c cdcacm.c rtos/heap_4.c rtos/list.c rtos/port.c rtos/queue.c rtos/tasks.c rtos/opencm3.c unique_id.c stm32_uidhash.c

LDSCRIPT	= stm32f103cct6.ld

# DEPS		= 	# Any additional dependencies for your build
# CLOBBER	+= 	# Any additional files to be removed with "make clobber"

include ./Makefile.incl
include ./Makefile.rtos

