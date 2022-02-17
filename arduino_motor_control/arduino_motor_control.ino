/*
 * Date   : 2021-08-02
 * Project: RCC (Remote Control Car)
 * Author : Yang-Hsi Su
 * 
 * Summary: 
 *		Motor control
 *
 */

//pin connections
#define EN1   8
#define DIR1  9
#define EN2  10
#define DIR2 11


uint8_t speed=150;

void setup()
{
	Serial.begin(9600);

	// Pin configuration
  	pinMode(DIR1, OUTPUT); 
  	pinMode(EN1,  OUTPUT);
  	pinMode(DIR2, OUTPUT); 
  	pinMode(EN2,  OUTPUT);
  	
  	// Stop motor
  	analogWrite(EN1, 0);
  	analogWrite(EN2, 0);

  	// Forward
  	digitalWrite(DIR1, LOW); 
  	digitalWrite(DIR2, LOW); 
}

/* Instruction:
 * 		1. Start with "S"
 * 		2. End   with "E\n"
 * 		3. Second char is type of instruction
 			Motor control: ''
 * 
 * 		Final instruction: SCXXXXE\n
 *
 */

void loop()
{
	decode(getSerial());
}

char getSerial()
{
	while(Serial.available()==0);
	return Serial.read();
}

void decode(char c)
{
	if(c!='S')
	{
		Serial.print("First char is not 'S'\n");
		return;
	}

	// Command set
	switch(getSerial())
	{
		// Control
		case 'C':
			Serial.print("Got C.\n");
			break;
		// Motor
		case 'M':
			Serial.print("Got M.\n");
			motor();
			break;
		default:
			Serial.print("Not within the command set.\n");
			return;
	}

	if(getSerial()!='E')
	{
		Serial.print("Ending 'E' not found.\n");
		return;
	}

	if(getSerial()!='\n')
	{
		Serial.print("Ending '%\n' not found.\n");
		return;
	}

	Serial.print("Valid instruction!\n");
	return;
}

void motor()
{
	switch(getSerial())
	{
		// Forward
		case 'F':
			Serial.print("Motor F\n");
			digitalWrite(DIR1, LOW);
			digitalWrite(DIR2, LOW);
			analogWrite(EN1, speed);
			analogWrite(EN2, speed);
			break;
		// Backward
		case 'B':
			Serial.print("Motor B\n");
			digitalWrite(DIR1, HIGH);
			digitalWrite(DIR2, HIGH);
			analogWrite(EN1, speed);
			analogWrite(EN2, speed);
			break;
		// Left
		case 'L':
			break;
		// Right
		case 'R':
			break;
		// Stop
		case 'S': 
			Serial.print("Motor S\n");
			analogWrite(EN1, 0);
			analogWrite(EN2, 0);
			digitalWrite(DIR1, LOW);
			digitalWrite(DIR2, LOW);
			break;	
		default:
			break;
	}
	return;
}