#define ledG 12
#define ledR 11
 
void setup() {
  pinMode(ledG, OUTPUT);
  pinMode(ledR, OUTPUT);
  Serial.begin(9600);
 
}
 
void loop() {
  if(Serial.available() > 0){
    char comando = Serial.read();
    if(comando == '1'){
      digitalWrite(ledG, HIGH);
      digitalWrite(ledR, LOW);
    }else if(comando == '0'){
      digitalWrite(ledR, HIGH);
      digitalWrite(ledG, LOW);
    }
  }
 
}