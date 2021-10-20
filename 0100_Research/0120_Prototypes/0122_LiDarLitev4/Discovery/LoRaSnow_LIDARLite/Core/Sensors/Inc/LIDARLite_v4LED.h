/*
 * LIDARLite_v4LED.h
 *
 *  Created on: 14 oct. 2021
 *      Author: vince
 */

#ifndef LIDARLITE_V4LED_H_
#define LIDARLITE_V4LED_H_

#include "stm32f7xx_hal.h"
#include <stdbool.h>

//Class defines
#define LIDAR_DEFAULT_ADDR (0x62 << 1)
#define I2C_MAX_BUF_LENGTH 12

//Register map
enum
{
	ACQ_COMMANDS = 0x00,
	STATUS = 0x01,
	ACQUISITION_COUNT = 0x05,
	FULL_DELAY_LOW = 0x10,
	FULL_DELAY_HIGH = 0x11,
	UNIT_ID_0 = 0x16,
	UNIT_ID_1 = 0x17,
	UNIT_ID_2 = 0x18,
	UNIT_ID_3 = 0x19,
	I2C_SEC_ADDR = 0x1A,
	I2C_CONFIG = 0x1B,
	DETECTION_SENSITIVITY = 0x1C,
	LIB_VERSION = 0x30,
	CORR_DATA = 0x52,
	CP_VER_LO = 0x72,
	CP_VER_HI = 0x73,
	BOARD_TEMPERATURE = 0xE0,
	HARDWARE_VERSION = 0xE1,
	POWER_MODE = 0xE2,
	MEASUREMENT_INTERVAL = 0xE3,
	FACTORY_RESET = 0xE4,
	QUICK_TERMINATION = 0xE5,
	START_BOOTLOADER = 0xE6,
	ENABLE_FLASH_STORAGE = 0xEA,
	HIGH_ACCURACY_MODE = 0xEB,
	SOC_TEMPERATURE = 0xEC,
	ENABLE_ANT_RADIO = 0xF0,
}LIDAR_cmd;

//LIDAR structure
typedef struct
{
	uint8_t addr;
	uint8_t buf[I2C_MAX_BUF_LENGTH];
	bool isConnected;
}LIDARLite_TypeDef;

//Variables
I2C_HandleTypeDef* _i2cPort;

//Function prototypes
bool LIDAR_init(LIDARLite_TypeDef* lidar, uint8_t addr, I2C_HandleTypeDef* i2cPort);

bool LIDAR_isConnected(LIDARLite_TypeDef* lidar);
void LIDAR_configure(LIDARLite_TypeDef* lidar, uint8_t configuration);
bool LIDAR_setI2CAddr(LIDARLite_TypeDef* lidar, uint8_t newAddr);

//TO MODIFY
bool LIDAR_useDefaultAddress(LIDARLite_TypeDef* lidar);
bool LIDAR_useNewAddressOnly(LIDARLite_TypeDef* lidar);
bool LIDAR_useBothAddresses(LIDARLite_TypeDef* lidar);
void LIDAR_enableFlash(LIDARLite_TypeDef* lidar, bool enable); //Toggle between RAM and FLASH/NVM storage

//Get distance measurement helper functions
void LIDAR_takeRange(LIDARLite_TypeDef* lidar);        //Initiate a distance measurement by writing to register 0x00
void LIDAR_waitForBusy(LIDARLite_TypeDef* lidar);      //Blocking function to wait until the LIDAR Lite's internal busy flag goes low
uint8_t LIDAR_getBusyFlag(LIDARLite_TypeDef* lidar);   //Read BUSY flag from device registers. Function will return 0x00 if not busy
uint16_t LIDAR_readDistance(LIDARLite_TypeDef* lidar); //Read and return the result of the most recent distance measurement in centimeters

//Get distance measurement function
uint16_t LIDAR_getDistance(LIDARLite_TypeDef* lidar); //Asks for, waits, and returns new measurement reading in centimeters

//Internal I2C abstraction
bool LIDAR_write(LIDARLite_TypeDef* lidar, uint8_t cmd, uint8_t numBytes); //Perform I2C write to the device. Can specify the number of bytes to be written
bool LIDAR_read(LIDARLite_TypeDef* lidar, uint8_t cmd, uint8_t numBytes);  //Perform I2C read from device. Can specify the number of bytes to be read

void LIDAR_correlationRecordRead(LIDARLite_TypeDef* lidar, int16_t *correlationArray, uint8_t numberOfReadings);


#endif /* LIDARLITE_V4LED_H_ */
