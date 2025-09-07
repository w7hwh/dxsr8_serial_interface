/* dxsr8_interface.c
 *
 * Last edit:	20250906 1115 hrs by hwh
 *
 * Edit history:
 *
 * TODO:
 *	read/write usb
 *	read/write head
 *	read/write chassis
 *	decode head
 *	decode chassis
 *	encode head to chassis
 *	encode chassis to head
 *	respond to cat commands from usb
 *
 *
 * Port usage:
 *		PA2		TX2		to head
 *		PA3		RX2		from head
 *		PA11	USBDM	usb to host
 *		PA12	USBDP	usb to host
 *		PA13	SWDIO	debug
 *		PA14	SWCLK	debug
 *
 *		PB10	TX3		to chassis
 *		PB11	RX3		from chassis
 *
 *		PC13	LED		on board led
 *		PC14	OSC32	rtc crystal
 *		PC15	OSC32	rtc crystal
 *
 */
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>

//#include <libopencm3/cm3/cortex.h>
//#include <libopencm3/cm3/scb.h>
#include <libopencm3/stm32/rcc.h>
#include <libopencm3/stm32/gpio.h>
//#include <libopencm3/cm3/scb.h>
//#include <libopencm3/stm32/exti.h>
//#include <libopencm3/stm32/adc.h>
//#include <libopencm3/stm32/timer.h>
//#include <libopencm3/stm32/dma.h>
//#include <libopencm3/stm32/rtc.h>
//#include <libopencm3/stm32/f1/bkp.h>
//#include <libopencm3/stm32/f1/nvic.h>

//#include "mcuio.h"
//#include "miniprintf.h"

#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"

#include "cdcacm.h"

/*
 * Monitor task:
 */
static void
monitor_task(void *arg __attribute((unused))) {

	for (;;) {
		//monitor();
		gpio_toggle(GPIOC,GPIO13);
		vTaskDelay(500);
	}
}

/*
 * Main program: Device initialization etc.
 */
int
main(void) {

	rcc_clock_setup_pll(&rcc_hse_configs[RCC_CLOCK_HSE8_72MHZ]);

	setup_usb();

	rcc_periph_clock_enable(RCC_GPIOC);
	gpio_set_mode(GPIOC,GPIO_MODE_OUTPUT_50_MHZ,GPIO_CNF_OUTPUT_PUSHPULL,GPIO13);

	xTaskCreate(monitor_task,"monitor",350,NULL,1,NULL);

	gpio_clear(GPIOC,GPIO13);

	vTaskStartScheduler();

	for (;;);
	return 0;
}

/* End main.c */
