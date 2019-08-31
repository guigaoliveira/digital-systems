#include <Arduino.h>

int period = 100;
unsigned long time_now = 0;

void setup()
{
  Serial.begin(115200);
  pinMode(13, OUTPUT);
}

void loop()
{
  if (Serial.read() == '1')
  {
    digitalWrite(13, HIGH);
    delay(1);
  }
  else
  {
    digitalWrite(13, LOW);
    delay(1);
  }
  if (millis() > time_now + period)
  {
    time_now = millis();
    float variable = 1.1;
    String buf;
    buf += "{\"sensor1\":";
    buf += String(variable, 6);
    buf += "}\n";
    Serial.write(buf.c_str());
    digitalWrite(13, LOW);
  }
}