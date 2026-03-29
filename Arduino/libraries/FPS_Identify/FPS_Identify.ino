#include "FPS_GT511C3.h"
#include "SoftwareSerial.h"

FPS_GT511C3 fps(8, 9);

void setup()
{
	Serial.begin(9600);
	delay(100);
	fps.Open();
	fps.SetLED(true);
        Serial.println("Please Press Finger");
        Serial.println();
}

void loop()
{

	// Identify fingerprint test
	if (fps.IsPressFinger())
	{
		fps.CaptureFinger(false);
		int id = fps.Identify1_N();
		if (id <200)
		{
			Serial.print("Verified ID: ");
        if (id == 0, 1, 2, 3)
        {
        Serial.print("Ethan ");
          if (id == 0)
          {
            Serial.println("( Right Thumb )");
          }
          
          if (id == 1)
          {
            Serial.println("( Left Thumb )");
          }
          
          if (id == 2)
          {
            Serial.println("( Right Index Finger )");
          }
          
          if (id == 3)
          {
            Serial.println("( Left Index Finger )");
          }
        }
        
	else
        {
        Serial.println(id);
        }		
        
        Serial.println("Welcome Back");
        Serial.println();
                            
		}
		else
		{
			Serial.println("Finger not found");
                        Serial.println("Please Repress Finger");
                        Serial.println();
		}

	}
	delay(100);
}
