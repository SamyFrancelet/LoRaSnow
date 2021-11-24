/*
 * LIDAR_functions.c
 *
 *  Created on: Oct 22, 2021
 *      Author: vince
 */

#include "../Inc/LIDAR_functions.h"

void LIDARfc_init(UART_HandleTypeDef* huart2, LIDARLite_TypeDef* lidar, I2C_HandleTypeDef* hi2c1, float lAngle, float rAngle)
{
	_huart2 = huart2;
	_hi2c1 = hi2c1;
	_lidar = lidar;

	//Connect to LIDAR
	bool connect = LIDAR_init(_lidar, LIDAR_DEFAULT_ADDR, _hi2c1, lAngle, rAngle);

	if(connect)
	   strcpy((char*)str, "Successfully connected.\r\n");
	else
	   strcpy((char*)str, "Error.\r\n");

	LIDARfc_printf(str);
}

uint16_t LIDARfc_distanceToGround(uint16_t* measures, uint8_t size)
{
	//Local variables
	uint16_t max = 0;

	LIDARfc_measure(measures, NMES, 200);	//Take distance measures
	max = measures[0];

	//Real distance is the max of the set of measures
	for(int i = 0; i < size; i++)
	{
		if(measures[i] > max)
		{
			max = measures[i];
		}
	}

	sprintf((char*)str, "\nDistance to ground is %icm\r\n", max);
	LIDARfc_printf(str);

	return max;
}

void LIDARfc_saveRefDistance()
{
	sprintf((char*)str, "Taking reference distance...\r\n\n");
	LIDARfc_printf(str);

	refDist = LIDARfc_distanceToGround(measures, NMES);		//Save reference distance
}

void LIDARfc_measureOffset()
{
	uint16_t dist = 0, delta = 0;
	float gamma = 0;

	sprintf((char*)str, "Measuring offset...\r\n\n");
	LIDARfc_printf(str);

	dist = LIDARfc_distanceToGround(measures, NMES);			//Save measured distance
	delta = refDist - dist;										//Compute the difference between the measured and the reference distance
	gamma = M_PI / 2 + _lidar->roadAngle - _lidar->lidarAngle;	//See the report to understand offset computation

	offset = delta * cosf(M_PI / 2 - gamma);					//Compute the snow height

	sprintf((char*)str, "Measured offset is %icm\r\n", offset);
	LIDARfc_printf(str);
}

void LIDARfc_measure(uint16_t* measures, uint8_t nTimes, uint16_t delay)
{
	sprintf((char*)str, "Taking %i measures with a %ims delay...\r\n", nTimes, delay);
	LIDARfc_printf(str);

	for(uint8_t i = 0; i < nTimes; i++)
	{
		float progress = ((float)i+1)/nTimes*100;

		measures[i] = LIDAR_getDistance(_lidar);		//Take distance measurements

		sprintf((char*)str, "\r%.2f%% done...  ", progress);
		LIDARfc_printf(str);

		HAL_Delay(delay);
	}

	sprintf((char*)str, "\r\n");
	LIDARfc_printf(str);
}

void LIDARfc_printf(uint8_t* toSend)
{
	HAL_UART_Transmit(_huart2, toSend, strlen((char*)toSend), HAL_MAX_DELAY);
}
