/*
 * LIDAR_functions.c
 *
 *  Created on: Oct 22, 2021
 *      Author: vince
 */

#include "../Inc/LIDAR_functions.h"

void LIDARfc_init(UART_HandleTypeDef* huart2, LIDARLite_TypeDef* lidar, I2C_HandleTypeDef* hi2c1)
{
	_huart2 = huart2;
	_hi2c1 = hi2c1;
	_lidar = lidar;

	//Connect to LIDAR
	bool connect = LIDAR_init(_lidar, LIDAR_DEFAULT_ADDR, _hi2c1);

	if(connect)
	   strcpy((char*)str, "Successfully connected.\r\n");
	else
	   strcpy((char*)str, "Error.\r\n");

	LIDARfc_printf(str);
}

void LIDARfc_calibDistance()
{

}

void LIDARfc_measureNoise()
{
	uint8_t i = 0;
	uint16_t distance = 0;

	if(!HAL_GPIO_ReadPin(GPIOC, GPIO_PIN_13))	//User button to start measurement
	{
	  for(i = 0; i < 100; i++)
	  {
		  distance = LIDAR_getDistance(_lidar);

		  sprintf((char*)str, "%i;", distance);
		  LIDARfc_printf(str);

		  HAL_Delay(500);
	  }

	  strcpy((char*)str, "\r\n");
	  LIDARfc_printf(str);
	}
}

uint16_t LIDARfc_mostOccurence(uint16_t* measures)
{
	return 0;
}

void LIDARfc_printf(uint8_t* toSend)
{
	HAL_UART_Transmit(_huart2, toSend, strlen((char*)toSend), HAL_MAX_DELAY);
}
