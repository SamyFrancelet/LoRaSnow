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
#include <math.h>

#include "stm32f4xx_hal.h"

#include "LIDARLite_v4LED.h"

#define NMES 50

UART_HandleTypeDef* _huart2;
I2C_HandleTypeDef* _hi2c1;
LIDARLite_TypeDef* _lidar;

uint8_t str[100];			//String buffer
uint16_t refDist;			//Reference distance (without snow)
float offset;				//Snow height
uint16_t measures[NMES];	//Measures array

void LIDARfc_init(UART_HandleTypeDef* huart2, LIDARLite_TypeDef* lidar, I2C_HandleTypeDef* hi2c1, float lAngle, float rAngle);	//Initialize the LIDARLite

void LIDARfc_measure(uint16_t* measures, uint8_t nTimes, uint16_t delay);	//Take nTimes measures with a specified delay
void LIDARfc_saveRefDistance();												//Take distance measurement and save and reference
void LIDARfc_measureOffset();												//Measure snow offset

uint16_t LIDARfc_distanceToGround(uint16_t* measures, uint8_t size);										//Output distance to ground according to a model

void LIDARfc_printf(uint8_t* str);											//Convenience function, equivalent to printf

#endif /* SENSORS_INC_LIDAR_FUNCTIONS_H_ */
