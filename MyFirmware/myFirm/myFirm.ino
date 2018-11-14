/*
 * FirmWare for Control Lab
  May 2018
  Vinicius Dutra Dias
*/

//constants
const int pinT1 = 0;
const int pinT2 = 2;
const int pinQ1 = 3;
const int pinQ2 = 5;
const int pinLed = 9;
const float analogTomV = 3300.0/1024.0; // Reference of 3.3V divided by 10 bit read (2^10)

const String firmVersion = "1.0";   //Firmware version
const int baudRate = 9600;          //Serial baud rate
const char separator = ' ';         //Command separator
const char endOfCmd = '\n';         //Command terminator
const int n = 10;                   //Samples for tempeterature reading

//global variables
char bufferIn[64];
float value = 0.0;                  //Value read from serial
int iWrite = 0;                     //Value to update
String cmd;                         //Command from serial

void setup() {
  analogReference(EXTERNAL);
  
  Serial.begin(baudRate);
  while(!Serial)  {;}
  analogWrite(pinQ1, 0);
  analogWrite(pinQ2, 0);
}

void loop() {
  //Parse command from serial input
  Serial.readBytesUntil(endOfCmd, bufferIn, sizeof(bufferIn));

  //Get command
  String data = String(bufferIn);
  int pos = data.indexOf(separator); 
  cmd  = data.substring(0, pos);
  cmd.trim();
  cmd.toUpperCase();

  //Get command value
  data =  data.substring(pos);
  data.trim();
  value = data.toFloat();

  //Clear buffer
  memset(bufferIn, 0, sizeof(bufferIn));

  //Commands
  if(cmd == "T1" || cmd == "T2")
    Serial.println(getTemp(cmd));
    
  else if(cmd == "T")
    Serial.println((getTemp("T1") + getTemp("T2"))/2);
    
  else if ((cmd == "V") or (cmd == "VER"))
    Serial.println("My Firmware Version " + firmVersion);
    
  else if((cmd == "Q1") || (cmd == "Q2") || (cmd == "LED")){
    checkValue();
    int writePin = (cmd == "Q1") ? pinQ1 : (cmd == "Q2") ? pinQ2 : pinLed;
    
    analogWrite(writePin, iWrite);
    Serial.println(value);
  }
}

float getTemp(String cmd)
{
  float mV = 0;
  float temp = 0;
  int pin;

  if(cmd == "T1")
    pin = pinT1;
  else
    pin = pinT2;

  for(int i = 0; i < n; i++){
    mV = (float) analogRead(pin)*analogTomV;
    temp = temp + (mV-500.0)/10.0; //mV to degrees Celsius
  }
    return temp/float(n);
}

void checkValue(){
  //Value between 100 and 0
  value = max(0, min(100, value));

  if(cmd == "Q1" || cmd == "Q2"){
    iWrite = int(value*2.0);
    iWrite = min(iWrite, 255);
  }
  else if(cmd == "LED"){
    iWrite = int(value*0.5);
    iWrite = min(iWrite, 50);
  }
}
