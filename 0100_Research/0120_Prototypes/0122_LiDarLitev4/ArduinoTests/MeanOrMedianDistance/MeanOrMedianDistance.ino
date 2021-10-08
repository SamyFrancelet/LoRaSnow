/******************************************************************************
  Reads the distance something is in front of LIDAR and prints it to the Serial port

  Priyanka Makin @ SparkX Labs
  Original Creation Date: Sept 30, 2019

  This code is Lemonadeware; if you see me (or any other SparkFun employee) at the
  local, and you've found our code helpful, please buy us a round!

  Hardware Connections:
  Plug Qwiic LIDAR into Qwiic RedBoard using Qwiic cable.
  Set serial monitor to 115200 baud.

  Distributed as-is; no warranty is given.
******************************************************************************/
#include "LIDARLite_v4LED.h"
#include "math.h"

LIDARLite_v4LED myLIDAR; //Click here to get the library: http://librarymanager/All#SparkFun_LIDARLitev4 by SparkFun

int nMes = 21;
float mes[21];

void setup() {
  Serial.begin(115200);
  Serial.println("Qwiic LIDARLite_v4 examples");
  Wire.begin(); //Join I2C bus

  //check if LIDAR will acknowledge over I2C
  if (myLIDAR.begin(0x62, Wire) == false) {
    Serial.println("Device did not acknowledge! Freezing.");
    while(1);
  }
  Serial.println("LIDAR acknowledged!");
}

void loop() {
  float sum = 0, sumSqu = 0;
  float mean = 0, stdDev = 0;
  
  Serial.print("Taking measures...");
  //Mean computation
  for(int i = 0; i < nMes; i++)
  {
    mes[i] = myLIDAR.getDistance();
    sum += mes[i];    

    delay(20);  //Don't hammer too hard on the I2C bus
  }
  mean = sum / nMes;
  Serial.print("Mean: ");
  Serial.println(mean);

  //Standard Deviation computation
  for(int i = 0; i < nMes; i++)
  {
    sumSqu += pow(mes[i]-mean, 2);
  }
  stdDev = sqrt(sumSqu / nMes);
  Serial.print("Standard Deviation: ");
  Serial.println(stdDev);

  //Delete anormal values
  for(int i = 0; i < nMes; i++)
  {
    if(mes[i] <= mean - 3*stdDev || mes[i] >= mean + 3*stdDev)
    {
      mes[i] = 0;
    }
    else
    {
      mes[i] *= 10; //mm
    }
  }

  //Precise mean computation
  int cnt = 0;
  for(int i = 0; i < nMes; i++)
  {
    if(mes[i] > 0)
    {
      sum += mes[i];  
      cnt++;  
    }
  }
  mean = sum / cnt;
  Serial.print("Precise Mean: ");
  Serial.println(mean);
  Serial.println();
}
