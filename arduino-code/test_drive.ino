int pwmA_pin = 3;
int dirA_pin = 12;
int pwmB_pin = 11;
int dirB_pin = 13;
int pwm_dc = 0;
boolean dir = true;
String inString = "";
int speed_a = 0;
int speed_b = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pwmA_pin, OUTPUT);
  pinMode(dirA_pin, OUTPUT);
  pinMode(pwmB_pin, OUTPUT);
  pinMode(dirB_pin, OUTPUT);
}

void loop() {

}

//check direction and change move speed
void drive(int speed_a, int speed_b) {
  if (speed_a > 0 && speed_b > 0) {
    dir = true;
    digitalWrite(dirA_pin, dir);
    digitalWrite(dirB_pin, !dir);
  } else if (speed_a < 0 && speed_b < 0) {
    dir = false;
    digitalWrite(dirA_pin, dir);
    digitalWrite(dirB_pin, !dir);
    speed_a *= -1;
    speed_b *= -1;
  } else if (speed_a > 0 && speed_b < 0) {
    dir = true;
    digitalWrite(dirA_pin, dir);
    digitalWrite(dirB_pin, dir);
    //    speed_a *= -1;
    speed_b *= -1;
  } else if (speed_a < 0 && speed_b > 0) {
    dir = false;
    digitalWrite(dirA_pin, dir);
    digitalWrite(dirB_pin, dir);
    speed_a *= -1;
    //    speed_b *= -1;
  }
  Serial.print("a : ");
  Serial.println(speed_a);
  Serial.print("b : ");
  Serial.println(speed_b);
  float s_a = speed_a * 255 / 100.0;
  float s_b = speed_b * 255 / 100.0;
  analogWrite(pwmA_pin, s_a);
  analogWrite(pwmB_pin, s_b);
}

void serialEvent() {
  while (Serial.available()) {
    // get the new byte:
    char inChar = (char)Serial.read();

    // if the incoming character is a newline, set a flag
    // so the main loop can do something about it:
    if (inChar == ':' || inChar == '\n') {
      drive(speed_a, speed_b);
      inString = "";
    } else {
      if (inChar != ',' && inChar != '(' && inChar != ')') {
        inString += inChar;
      } else {
        if (inChar == ',') {
          speed_a = inString.toInt();
//          Serial.print("a : ");
//          Serial.println(speed_a);
          inString = "";
        } else if (inChar == ')') {
          speed_b = inString.toInt();
//          Serial.print("b : ");
//          Serial.println(speed_b);
          inString = "";
        }
      }
    }
  }
}
