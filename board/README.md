# DXSR8 Serial Interface Design Files

## GPIO Usage

- GP0  
- GP1  
- GP2  
- GP3  
- GP4	UART1-TX serial send to chassis
- GP5	UART1-RX serial receive from head
- GP6  
- GP7  
- GP8  
- GP9  
- GP10  
- GP11  
- GP12	UART0-TX serial send to head
- GP13	UART0-RX serial receive from chassis
- GP14  
- GP15  
- GP16	I2C0-SDA for SH1106 based display
- GP17	I2C0-SCL for SH1106 based display
- GP18  
- GP19  
- GP20  
- GP21  
- GP22  
- GP23  (wireless module) OP wireless power on signal
- GP24  (wireless module) OP/IP SPI data/IRQ
- GP25  (wireless module) OP SPI CS, when high also enable GP29 to read VSYS
- GP26	ADC0 monitor power from chassis
- GP27  ADC1 monitor power from USB
- GP28  
- GP29  (wireless module) OP/IP SPI CLK/ADC3 mode read VSYS/3
- WL_GPOI0  (wireless module) OP to LED
- WL_GPOI1  (wireless module) OP controls SMPS power save
- WL_GPOI2  (wireless module) IP high if VBUS present
