  // Basic Bluetooth sketch HC-05_01
// Sends "Bluetooth Test" to the serial monitor and the software serial once every second.
//
// Connect the HC-05 module and data over Bluetooth
//
// The HC-05 defaults to commincation mode when first powered on.
// The default baud rate for communication is 9600
// http://www.martyncurrey.com/arduino-with-hc-05-bluetooth-module-in-slave-mode/
 
#include <SoftwareSerial.h>
SoftwareSerial BTserial(2, 3); // RX | TX
// Connect the HC-05 TX to Arduino pin 2 RX. 
// Connect the HC-05 RX to Arduino pin 3 TX through a voltage divider.
// 
 
//char c = ' ';
//int i=0;
//char snum[5];
//
//void setup() 
//{
//    Serial.begin(9600);
//    Serial.println("Enter AT commands:");
// 
//    // HC-06 default serial speed for communcation mode is 9600
//    BTserial.begin(38400);  
//}
// 
//void loop() 
//{
////    itoa(i, snum, 10);
//    c=i+'0';
//    BTserial.print("Bluetooth Test "); 
//    BTserial.print(c); 
//    BTserial.print("\n"); 
//    Serial.println(c); 
//    delay(1000); 
//    i++;
//    if(i==10) i=0;
//}

// Basic Bluetooth sketch HC-05_02
// Connect the HC-05 module and communicate using the serial monitor
//
// The HC-05 defaults to commincation mode when first powered on.
// The default baud rate for communication mode is 9600
//
 
char c = ' ';
 
void setup() 
{
    Serial.begin(9600);
    Serial.println("Arduino is ready");
 
    // HC-05 default serial speed for commincation mode is 9600
    BTserial.begin(38400);  
}
 
void loop()
{
 
    // Keep reading from HC-05 and send to Arduino Serial Monitor
    if (BTserial.available())
    {  
        c = BTserial.read();
        Serial.write(c);
    }
 
    // Keep reading from Arduino Serial Monitor and send to HC-05
    if (Serial.available())
    {
        c =  Serial.read();
        BTserial.write(c);  
    }
 
}
