int analogPin = A3; // pino analógico 
int analogValue = 0; // variável para guardar o valor da leitura analógica
int buttonState = 0; // variavél para guardar o valor da leitura do botão 
int incomingByte = 0; // variavél para guardar um valor enviado via porta serial   

const int LED = 13;
const int buttonPin = 7;

void setup() {
  Serial.begin(9600);
  pinMode(LED, OUTPUT);
  pinMode(buttonPin, INPUT);
}

void loop() {
  // lê a serial e aciona o led a partir do que vier (1 ou 0) 
  incomingByte = Serial.read(); 
  digitalWrite(LED, incomingByte); 

  // lê o pino analógico e envia o valor via serial (como decimal)
  analogValue = analogRead(analogPin);
  Serial.println(analogValue, DEC);
  delay(200);
  
  // lê o pino digital e envia o valor via serial (como decimal)
  buttonState = digitalRead(buttonPin);
  Serial.println(buttonState, DEC);
  delay(200);
}
