/*
 * FirmWare for Control Lab
  May 2018
  Oct 2019
  Vinicius Dutra Dias
*/

//constants
const int pinT1 = 0;
const int pinT2 = 2;
const int pinQ1 = 3;
const int pinQ2 = 5;
const int pinLed = 9;
const float analogTomV = 3300.0/1024.0; // Reference of 3.3V divided by 10 bit read (2^10)

const String firmVersion = "1.2";   //Firmware version
const int baudRate = 9600;          //Serial baud rate
const char separator = ' ';         //Command separator
const char endOfCmd = '\n';         //Command terminator
const int n = 10;                   //Samples for tempeterature reading

//global variables
char bufferIn[6];
float value = 0.0;                  //Value read from serial
int iWrite = 0;                     //Value to update
String cmd;                         //Command from serial
String data;

void setup() {
  analogReference(EXTERNAL);
  
  Serial.begin(baudRate);
  while(!Serial)  {;}
}

void loop() {
  readCmd();
  parseCmd();
  execCmd();
  Serial.flush();
}

void readCmd(){
  //Parse command from serial input
  Serial.readBytesUntil(endOfCmd, bufferIn, sizeof(bufferIn));
}

void parseCmd(){
  //Get command
  data = String(bufferIn);
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
}

void execCmd(){
  //Commands
  if(cmd == "T1")
    Serial.println(getTemp(pinT1));

  else if(cmd == "T2")
    Serial.println(getTemp(pinT2));
    
  else if(cmd == "T")
    Serial.println((getTemp(pinT1) + getTemp(pinT2))/2);
    
  else if (cmd == "V")
    Serial.println("My Firmware Version " + firmVersion);
    
  else if(cmd == "Q1"){
    checkValue(); 
    
    analogWrite(pinQ1, iWrite);
    Serial.println(value);
  }

  else if(cmd == "Q2"){
    checkValue(); 
    
    analogWrite(pinQ2, iWrite);
    Serial.println(value);
  }
  else if(cmd == "L"){
    checkValue();

    analogWrite(pinLed, iWrite);
    Serial.println(value);
  }
}

float getTemp(int pin)
{
  float mV = 0;
  float temp = 0;

  for(int i = 0; i < n; i++){
    mV = (float) analogRead(pin)*analogTomV;
    temp = temp + (mV-500.0)/10.0; //mV to degrees Celsius
  }
    return temp/float(n);
}

void checkValue(){
  //Value between 100 and 0
  value = max(0, min(100, value));

  iWrite = int(value*2.55);
  iWrite = min(iWrite, 255);
}
