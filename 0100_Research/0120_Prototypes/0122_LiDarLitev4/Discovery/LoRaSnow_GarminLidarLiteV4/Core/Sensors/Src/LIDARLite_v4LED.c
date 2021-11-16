/*------------------------------------------------------------------------------

  LIDARLite_v4LED library adapted for STM32
  LIDARLite_v4LED.cpp

  Original library:
  	  https://github.com/sparkfun/SparkFun_LIDARLitev4_Arduino_Library

  BLAH

------------------------------------------------------------------------------*/

#include "../Inc/LIDARLite_v4LED.h"

//Initialize the I2C port
bool LIDAR_init(LIDARLite_TypeDef* lidar, uint8_t addr, I2C_HandleTypeDef* i2cPort)
{
	lidar->addr = addr;		//Save LIDAR address
	_i2cPort = i2cPort;		//Save I2C port

	//Read status to check if lidar is connected
	lidar->isConnected = LIDAR_read(lidar, STATUS, 1);

	return lidar->isConnected;
}

//Check if the LIDAR is connected
bool LIDAR_isConnected(LIDARLite_TypeDef* lidar)
{
	return lidar->isConnected;
}

/*------------------------------------------------------------------------------
  Configure
  Selects one of several preset configurations.
  Parameters
  ------------------------------------------------------------------------------
  configuration:  Default 0.
    0: Maximum range. Uses maximum acquisition count.
    1: Balanced performance.
    2: Short range, high speed. Reduces maximum acquisition count.
    3: Mid range, higher speed. Turns on quick termination
         detection for faster measurements at short range (with decreased
         accuracy)
    4: Maximum range, higher speed on short range targets. Turns on quick
         termination detection for faster measurements at short range (with
         decreased accuracy)
    5: Very short range, higher speed, high error. Reduces maximum
         acquisition count to a minimum for faster rep rates on very
         close targets with high error.
------------------------------------------------------------------------------*/
void LIDAR_configure(LIDARLite_TypeDef* lidar, uint8_t configuration)
{
	uint8_t sigCountMax;
	uint8_t acqConfigReg;

	switch (configuration)
	{
	case 0: // Default mode - Maximum range
		sigCountMax = 0xff;
		acqConfigReg = 0x08;
		break;

	case 1: // Balanced performance
		sigCountMax = 0x80;
		acqConfigReg = 0x08;
		break;

	case 2: // Short range, high speed
		sigCountMax = 0x18;
		acqConfigReg = 0x00;
		break;

	case 3: // Mid range, higher speed on short range targets
		sigCountMax = 0x80;
		acqConfigReg = 0x00;
		break;

	case 4: // Maximum range, higher speed on short range targets
		sigCountMax = 0xff;
		acqConfigReg = 0x00;
		break;

	case 5: // Very short range, higher speed, high error
		sigCountMax = 0x04;
		acqConfigReg = 0x00;
		break;
	}

	lidar->buf[0] = sigCountMax;
	lidar->buf[1] = acqConfigReg;

	LIDAR_write(lidar, ACQUISITION_COUNT, 1);
	LIDAR_write(lidar, QUICK_TERMINATION, 1);
}

/*------------------------------------------------------------------------------
  Set I2C Address
  Set Alternate I2C Device Address. See Operation Manual for additional info.
  Parameters
  ------------------------------------------------------------------------------
  newAddress: desired secondary I2C device address
  disableDefault: a non-zero value here means the default 0x62 I2C device
    address will be disabled.
------------------------------------------------------------------------------*/
bool LIDAR_setI2CAddr(LIDARLite_TypeDef* lidar, uint8_t newAddr)
{
	//Not needed now
	return true;
}


bool LIDAR_useDefaultAddress(LIDARLite_TypeDef* lidar)
{
	//Not needed now
	return true;
}

bool LIDAR_useNewAddressOnly(LIDARLite_TypeDef* lidar)
{
	//Not needed now
	return true;
}

bool LIDAR_useBothAddresses(LIDARLite_TypeDef* lidar)
{
	//Not needed now
	return true;
}

void LIDAR_enableFlash(LIDARLite_TypeDef* lidar, bool enable)
{
	//Not needed now
}


/*------------------------------------------------------------------------------
  Take Range
  Initiate a distance measurement by writing to register 0x00.
------------------------------------------------------------------------------*/
void LIDAR_takeRange(LIDARLite_TypeDef* lidar)
{
	lidar->buf[0] = 0x04;
	LIDAR_write(lidar, ACQ_COMMANDS, 1);
}

/*------------------------------------------------------------------------------
  Wait for Busy Flag
  Blocking function to wait until the Lidar Lite's internal busy flag goes low
------------------------------------------------------------------------------*/
void LIDAR_waitForBusy(LIDARLite_TypeDef* lidar)
{
	uint8_t busyFlag;

	do
	{
		busyFlag = LIDAR_getBusyFlag(lidar);
	} while (busyFlag);
}

/*------------------------------------------------------------------------------
  Get Busy Flag
  Read BUSY flag from device registers. Function will return 0x00 if not busy.
------------------------------------------------------------------------------*/
uint8_t LIDAR_getBusyFlag(LIDARLite_TypeDef* lidar)
{
	uint8_t busyFlag; // busyFlag monitors when the device is done with a measurement

	// Read status register to check busy flag
	LIDAR_read(lidar, STATUS, 1);

	// STATUS bit 0 is busyFlag
	busyFlag = lidar->buf[0] & 0x01;

	return busyFlag;
}

/*------------------------------------------------------------------------------
  Read Distance
  Read and return the result of the most recent distance measurement.
------------------------------------------------------------------------------*/
uint16_t LIDAR_readDistance(LIDARLite_TypeDef* lidar)
{
	uint16_t distance;

	// Read two bytes from registers 0x10 and 0x11
	LIDAR_read(lidar, FULL_DELAY_LOW, 2);

	distance = lidar->buf[0] + (lidar->buf[1]<<8);

	return distance; //This is the distance in centimeters
}


//Get distance measurement function
uint16_t LIDAR_getDistance(LIDARLite_TypeDef* lidar)
{
	// 1. Trigger a range measurement.
	LIDAR_takeRange(lidar);

	// 2. Wait for busyFlag to indicate the device is idle.
	LIDAR_waitForBusy(lidar);

	// 3. Read new distance data from device registers
	return LIDAR_readDistance(lidar);
}

/*------------------------------------------------------------------------------
  Write
  Perform I2C write to device. The I2C peripheral in the LidarLite v3 HP
  will receive multiple bytes in one I2C transmission. The first byte is
  always the register address. The the bytes that follow will be written
  into the specified register address first and then the internal address
  in the Lidar Lite will be auto-incremented for all following bytes.

  Parameters
  ------------------------------------------------------------------------------
  regAddr:   register address to write to
  dataBytes: pointer to array of bytes to write
  numBytes:  number of bytes in 'dataBytes' array to write
------------------------------------------------------------------------------*/
bool LIDAR_write(LIDARLite_TypeDef* lidar, uint8_t cmd, uint8_t numBytes)
{
	HAL_StatusTypeDef ret;

	ret = HAL_I2C_Mem_Write(_i2cPort, lidar->addr, cmd, I2C_MEMADD_SIZE_8BIT, lidar->buf, numBytes, HAL_MAX_DELAY);

	if(ret != HAL_OK)	//Error in transmission
		return false;
	else
		return true;
}

/*------------------------------------------------------------------------------
  Read
  Perform I2C read from device.  The I2C peripheral in the LidarLite v3 HP
  will send multiple bytes in one I2C transmission. The register address must
  be set up by a previous I2C write. The bytes that follow will be read
  from the specified register address first and then the internal address
  pointer in the Lidar Lite will be auto-incremented for following bytes.
  Will detect an unresponsive device and report the error over serial.

  Parameters
  ------------------------------------------------------------------------------
  regAddr:   register address to read
  dataBytes: pointer to array of bytes to write
  numBytes:  number of bytes in 'dataBytes' array to read
------------------------------------------------------------------------------*/
bool LIDAR_read(LIDARLite_TypeDef* lidar, uint8_t cmd, uint8_t numBytes)
{
	HAL_StatusTypeDef ret;

	ret = HAL_I2C_Mem_Read(_i2cPort, lidar->addr, cmd, I2C_MEMADD_SIZE_8BIT, lidar->buf, numBytes, HAL_MAX_DELAY);

	if(ret != HAL_OK)	//Error in reception
		return false;
	else
		return true;
}

/*------------------------------------------------------------------------------
  Correlation Record Read
  The correlation record used to calculate distance can be read from the device.
  It has a bipolar wave shape, transitioning from a positive going portion to a
  roughly symmetrical negative going pulse. The point where the signal crosses
  zero represents the effective delay for the reference and return signals.

  Process
  ------------------------------------------------------------------------------
  1.  Take a distance reading (there is no correlation record without at least
      one distance reading being taken)
  2.  For as many points as you want to read from the record (max is 192) read
      the two byte signed correlation data point from 0x52

  Parameters
  ------------------------------------------------------------------------------
  correlationArray: pointer to memory location to store the correlation record
                    ** Two bytes for every correlation value must be
                       allocated by calling function
  numberOfReadings: Default = 192. Maximum = 192
------------------------------------------------------------------------------*/
void LIDAR_correlationRecordRead(LIDARLite_TypeDef* lidar, int16_t *correlationArray, uint8_t numberOfReadings)
{

}

