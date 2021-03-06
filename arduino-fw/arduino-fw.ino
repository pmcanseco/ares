#include <Servo.h>
Servo torxis_f;
Servo torxis_r;
String inputString;
boolean stringComplete = false;
int neutral = 187;

void setup() {
    pinMode(5, OUTPUT);  // FR
    pinMode(7, OUTPUT);  // FL
    pinMode(10, OUTPUT); // RR
    pinMode(8, OUTPUT);  // RL
    pinMode(A0, INPUT);  // BATT
    pinMode(2, OUTPUT);  // R ACTUATOR SPEED
    pinMode(22, OUTPUT); // R ACTUATOR DIR
    pinMode(3, OUTPUT);  // L ACTUATOR SPEED
    pinMode(23, OUTPUT); // L ACTUATOR DIR
    pinMode(4, OUTPUT);  // FRONT EXCAVATE
    pinMode(6, OUTPUT);  // REAR EXCAVATE
    
    pinMode(11, OUTPUT); // FRONT TORXIS
    pinMode(12, OUTPUT); // REAR TORXIS
    torxis_f.attach(11); // FRONT TORXIS
    torxis_f.write(90);  
    torxis_r.attach(12); // REAR TORXIS
    torxis_r.attach(90); 

    analogWrite(4, neutral);
    analogWrite(5, neutral);
    analogWrite(6, neutral);
    analogWrite(7, neutral);
    analogWrite(8, neutral);
    analogWrite(10, neutral);
    analogWrite(12, neutral);
    analogWrite(13, neutral);
    inputString.reserve(32);
    Serial.begin(115200);
    Serial.println("ARES Ready");
}

void loop() {
    if (Serial.available() > 0) {
        inputString = Serial.readStringUntil(';');
        stringComplete = true;
    }
    
    if (stringComplete) {
        //Serial.println(inputString);
        int i1 = inputString.indexOf(',');
        int i2 = inputString.lastIndexOf(',');
        char cmd = inputString.charAt(0);
        int gpio = inputString.substring(i1 + 1, i2).toInt();
        //String value = inputString.substring(i2+1, inputString.length());
        //Serial.println(value);
        int value = inputString.substring(i2 + 1, inputString.length()).toInt();
        /*Serial.print("CMD:  ");
        Serial.println(cmd);
        Serial.print("GPIO: ");
        Serial.println(gpio);
        Serial.print("VAL:  ");
        Serial.println(value);
        Serial.print("\n");*/
        switch (cmd) {
            case 'a': { // analogWrite
                analogWrite(gpio, value); }
                break;
            case 's': {
                //if (gpio == 8)
                    //conveyor.write(value);
                //if (gpio == 10)
                    //smallTestServo.write(value); 
                }
                break;
            case 'g': go(value);    break; // GO {VALUE} SPEED
            case '>': turn_r();     break; // TURN CW
            case '<': turn_l();     break; // TURN CCW
            case 'h': halt();       break; // STOP ALL MOTORS
            case 'r': read_batt();  break; // READ BATT VOLTAGE
            case 'u': retract();    break; // RETRACT ACTUATORS
            case 'y': halt_acts();  break; // STOP ACTUATORS
            case 't': extend();     break; // EXTEND ACTUATORS
            case 'p': mine_f();     break; // MINE FRONT DRUM
            case 'o': mine_r();     break; // MINE REAR DRUM
            case 'l': dump_f();     break; // DUMP FRONT DRUM
            case 'k': dump_r();     break; // DUMP REAR DRUM
            case 'z': raise_f();    break; // RAISE FRONT DRUM
            case 'x': lower_f();    break; // LOWER FRONT DRUM
            case 'c': raise_r();    break; // RAISE REAR DRUM
            case 'f': lower_r();    break; // LOWER REAR DRUM
        }
        stringComplete = false;
    }

}

/* HELPER FUNCTIONS */
void go(int speed) { // go transport motors
    analogWrite(5, speed);
    analogWrite(7, speed);
    analogWrite(8, speed);
    analogWrite(10, speed);
}
void halt() {        // stop transport motors
    analogWrite(5, neutral);
    analogWrite(7, neutral);
    analogWrite(8, neutral);
    analogWrite(10, neutral);

    analogWrite(11, neutral);
    torxis_f.write(90);
    // TODO rest of motors
}
void turn_r() {      // turn right
    analogWrite(5, 170);
    analogWrite(7, 210);
    analogWrite(8, 170);
    analogWrite(10, 210);
}
void turn_l() {      // turn left
    analogWrite(5, 210);
    analogWrite(7, 170);
    analogWrite(8, 210);
    analogWrite(10, 170);
}
void extend() {      // extend actuators
    digitalWrite(22, LOW);
    digitalWrite(23, LOW);
    analogWrite(2, 240);
    analogWrite(3, 240);
}
void retract(){      // retract actuators
    digitalWrite(22, HIGH);
    digitalWrite(23, HIGH);
    analogWrite(2, 60);
    analogWrite(3, 60);
}
void halt_acts() {   // stop actuators
    digitalWrite(22, HIGH);
    digitalWrite(23, HIGH);
    analogWrite(2, 250);
    analogWrite(3, 250);
}
void read_batt() {   // read battery voltage
    Serial.print("BATT: ");
    float batt = analogRead(A0) * (5.0 / 1023.0); // read direct pin voltage
    batt = batt / ( 910 / (float) (1600 + 910) );   // upconvert from 5V back to 12V
    Serial.println(batt);                           // print real voltage
}
void mine_f() {      // mine front drum     
    analogWrite(4, 230);
}
void mine_r() {      // mine rear drum      
    analogWrite(6, 230);
}
void dump_f() {      // dump front drum     
    analogWrite(4, 170);
}
void dump_r() {      // dump rear drum      
    analogWrite(6, 170);
}
void raise_f(){      // raise front drum    
    torxis_f.write(100);
}
void lower_f(){      // lower front drum    
    torxis_f.write(80);
}
void raise_r(){      // raise rear drum     
    torxis_r.write(100);
}
void lower_r(){      // lower rear drum     
    torxis_r.write(80);
}


