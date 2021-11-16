/*
 * LIDAR_functions.h
 *
 *  Created on: Oct 22, 2021
 *      Author: vince
 */

#ifndef SENSORS_INC_LIDAR_FUNCTIONS_H_
#define SENSORS_INC_LIDAR_FUNCTIONS_H_

#include <stdbool.h>
#include <string.h>
#include <stdio.h>

#include "stm32f4xx_hal.h"

#include "LIDARLite_v4LED.h"

UART_HandleTypeDef* _huart2;
I2C_HandleTypeDef* _hi2c1;
LIDARLite_TypeDef* _lidar;

uint8_t str[100];			//String buffer
uint16_t distance;			//The distance, in cm

void LIDARfc_init(UART_HandleTypeDef* huart2, LIDARLite_TypeDef* lidar, I2C_HandleTypeDef* hi2c1);	//Initialize the LIDARLite
void LIDARfc_calibDistance();							//Calibrate LIDAR distance
void LIDARfc_measureNoise();							//Measure noise in the test bench
uint16_t LIDARfc_mostOccurence(uint16_t* measures);		//Find the distance with the most occurrence in the array

void LIDARfc_printf(uint8_t* str);						//Convenience function, equivalent to printf

#endif /* SENSORS_INC_LIDAR_FUNCTIONS_H_ */
