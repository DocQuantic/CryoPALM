/*
This program reads the serial data coming from a python script and sets the adressed PWM output with the read value.
It is used to set an analog output value between 0 and 5 volts to control an analog device like the power of a laser.

We use a PWM output which is averaged thanks to a RC passive filter. 
To reduce the time constant of the filter, we overclock the frequency of the PWM to its maximum value 
which is 62500 Hz for pins 5, 6 and 31250 Hz for the others PWM pins.

The Serial.read() function can only read characters on by one so the number that we want to send is appended to start and stop delimiters
and then the characters of the final chain are sent one by one to the Arduino which then reconstructs the full chain containing the number value 
thanks to the start and stop delimiters.

Created by William Magrini on 2019/04/15
*/

#define pin405 6 //Pin number for 405 nm laser PWM output (channel 0)
#define pin488 3 //Pin number for 488 nm laser PWM output (channel 1)
#define pin561 5 //Pin number for 561 nm laser PWM output (channel 2)
#define blankPin 2 //Pin number for blanking digital output (channel 3)
#define switch405Pin 4 //Pin number for switching 405nm laser digital output (channel 4)
#define shutterPin 7 //Pin number for shutter control digital output (channel 5)

#define startDelimiter '<' //Start delimiter for the chain to read
#define stopDelimiter '>' //Stop delimiter for the chain to read
#define channelPowerSeparator ',' //Separator between channel to affect and power to apply in the chain to read

byte frequencyDivider = 0x01; //Frequency divider to obtain the maximum frequency value

String stringPower; //String that will contain the laser power amount
String stringChannel; //String that will contain the channel to affect

bool isAnalog; //Determines whether the selected channel is analog or not
int analogValue = 0; //Output value for the selected analog channel
int digitalValue = LOW; //Output value of the selected digital channel
int numberChannel; //Number of the channel to affect
int selectChannel; //Number of the pin to use for the selected channel

bool switchToPower = false; //Boolean that allows to differentiate if we are reading the channel number or the power value

void setup() {
  Serial.begin(115200); //Set the baud rate
  
  pinMode(pin405, OUTPUT); //Set the 405 nm laser pin
  pinMode(pin488, OUTPUT); //Set the 488 nm laser pin
  pinMode(pin561, OUTPUT); //Set the 561 nm laser pin
  pinMode(blankPin, OUTPUT); //Set the blanking pin
  pinMode(switch405Pin, OUTPUT); //Set the 405 switch pin
  pinMode(shutterPin, OUTPUT); //Set the shutter pin
  
  TCCR0B = TCCR0B & 0b11111000 | frequencyDivider; //Set the PWM frequency to its maximum for pins 5 and 6
  TCCR2B = TCCR2B & 0b11111000 | frequencyDivider; //Set the PWM frequency to its maximum for pin 3
  
  analogWrite(pin405, 0); //Initialize the output values
  analogWrite(pin488, 0); //Initialize the output values
  analogWrite(pin561, 0); //Initialize the output values
  digitalWrite(blankPin, LOW); //Initialize the output values
  digitalWrite(switch405Pin, LOW); //Initialize the output values
  digitalWrite(shutterPin, LOW); //Initialize the output values
  
  Serial.println("Ready"); //Print "Ready" once
}

//Function that converts the read string from serial to an int and writes the value to the channel 1
void setPWMOutput(String channel, String value){
  numberChannel = channel.toInt(); //Conversion to int of the channel number
  
  //Reads the channel number and extract the pin value and the type of the output (analog or digital)
  switch(numberChannel){
    case 0:
      selectChannel = pin405;
      isAnalog = true;
      break;
    case 1:
      selectChannel = pin488;
      isAnalog = true;
      break;
    case 2:
      selectChannel = pin561;
      isAnalog = true;
      break;
    case 3:
      selectChannel = blankPin;
      isAnalog = false;
      break;
    case 4:
      selectChannel = switch405Pin;
      isAnalog = false;
      break;
    case 5:
      selectChannel = shutterPin;
      isAnalog = false;
      break;
  }
  
  //Set the selected analog or digital output to the chosen value
  if(isAnalog==true){
    analogValue = value.toInt(); //Conversion to int
    
    analogWrite(selectChannel, analogValue); //Set the output value of selected analog output channel
  }
  else{
    if(value.toInt()>=127){
      digitalWrite(selectChannel, HIGH);
    }
    else if(value.toInt()<127){
      digitalWrite(selectChannel, LOW);
    }
  }
}

//Function that reads the characters coming from the serial port and creates the string containing the number
void processInput(){
  char c = Serial.read(); //Read the incoming data
    
  if(c==startDelimiter){
    stringPower = ""; //If the start delimiter is met, we reinitialize the string containing the number
    stringChannel = ""; //If the start delimiter is met, we reinitialize the string containing the channel
    switchToPower = false; //If the start delimiter is met, we reinitialize the separator boolean
  }
  else if(c==stopDelimiter){
    setPWMOutput(stringChannel, stringPower); //When the stop delimiter is met, the power is set on the selected channel
  }
  else if(c==channelPowerSeparator){
    switchToPower = true; //When the separator is met, we switch the boolean to populate the power instead of channel
  }
  else{
    //Else, the number is appended to the string to build it depending on if the separator was met or not
    if(switchToPower==true){
      stringPower += c; //If the separator was met, we build the power string
    }
    else{
      stringChannel += c; //Else, we build the channel string
    }
  }
}

void loop() {  
  if(Serial.available()){ //Only send data back if data has been sent
    processInput(); //Read and process the input serial values
  }
}
