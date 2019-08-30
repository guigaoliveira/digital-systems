#include <Arduino.h>

int IN3 = 4;
int IN4 = 5;
int velocidadeB = 9;
void setup()
{
  //Define os pinos como saida
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(velocidadeB, OUTPUT);
}

void loop()
{
  //Gira o Motor A no sentido horario
  analogWrite(velocidadeB, 255);
  //Gira o Motor B no sentido horario
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  delay(2000);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  delay(2000);
}