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

const String firmVersion = "0.1";   //Firmware version
const int baudRate = 9600;          //Serial baud rate
const char separator = ' ';         //Command separator
const char endOfCmd = '\n';         //Command terminator
const int n = 10;                   //Samples for tempeterature reading

//global variables
char bufferIn[64];
float value = 0.0;                  //Value read from serial
String cmd;                         //Command from serial

void setup() {
  analogReference(EXTERNAL);
  
  Serial.begin(baudRate);
  while(!Serial)  {;}
  analogWrite(pinQ1, 0);
  analogWrite(pinQ2, 0);
}

void checkValue(){
  if(value >= 100.0)
    value = 100.0;

  else if(value <= 0.0)
    value = 0.0;
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
  if(cmd == "T1"){
    float mV = 0;
    float temp = 0;

    for(int i = 0; i < n; i++){
      mV = (float) analogRead(pinT1)*analogTomV;
      temp = temp + (mV-500.0)/10.0; //mV to degrees Celsius
    }
    Serial.println(temp / float(n));
  }
  else if(cmd == "T2"){
    float mV = 0;
    float temp = 0;

    for(int i = 0; i < n; i++){
      mV = (float) analogRead(pinT2)*analogTomV;
      temp = temp + (mV-500.0)/10.0; //mV to degrees Celsius
    }
    Serial.println(temp / float(n));
  }
  else if ((cmd == "V") or (cmd == "VER")) {
    Serial.println("TCLab Firmware Version " + firmVersion);
  }
  else if (cmd == "Q1") {
    checkValue();
    analogWrite(pinQ1, value);
    Serial.println(value);
  }
  else if (cmd == "Q2") {
    checkValue();
    analogWrite(pinQ1, value);
    Serial.println(value);
  }
  
}
