/**
 * Dino Cajic
 * Autonomous RC Vehicle
 *
 * -------------------Give a description about what's happending in the code
 */
#include <Servo.h>

Servo steering;
Servo esc;

// Initialize the Electronic Speed Controller which is responsible for the motor
int escValue = 1500;
int escPin   = 9;

/**
 * value sent to the Steering Motor
 * 45 to 90 to turn right
 * 90 to 135 to turn left
 */
int steeringValue = 0;
int steeringPin   = 6;

// Right proximity sensor
int echoRight    = 4;
int triggerRight = 5;

// Left Proximity Sensor
int echoLeft    = 10;
int triggerLeft = 11;

int durationRight, distanceRight, durationLeft, distanceLeft;

int avoidDist = 30;

/** 
 * The incoming integer string. 
 * Comes in 1 character at a time so it'll have to be converted inside the loop
 */
String incomingInt = "";

void setup() {
  steering.attach(steeringPin);
  delay(10);
  esc.attach(escPin);
  
  pinMode(triggerRight, OUTPUT);
  pinMode(echoRight,    INPUT);
  
  pinMode(triggerLeft, OUTPUT);
  pinMode(echoLeft,    INPUT);
  
  delay(5000);
  
  Serial.begin(9600);
}

void loop() {
  // send the value to the steering motor, always starts at 0
  steering.write(steeringValue);
  esc.write(escValue);
  
  if ( Serial.available() > 0 ) {
    incomingInt = "";
    
    while( Serial.available() > 0 ) {
      int usbRead = Serial.read();
      
      incomingInt += (char)usbRead;
    }
  }
  
  calculateRightDistance();
  calculateLeftDistance();
  
  if ( distanceRight < avoidDist && distanceLeft < avoidDist ) {
    //steeringValue = 45;
    //escValue = 1000;
    Serial.println("Rear");
  } else if( distanceRight < avoidDist && distanceLeft >= avoidDist ) {
    //steeringValue = 135;
    Serial.println("Front");
    //escValue = 1000;
  } else if ( distanceRight >= avoidDist && distanceLeft < avoidDist ) {
    //steeringValue = 45;
    //escValue = 1000;
    Serial.println("Rear");
  } else {
    //steeringValue = 90;
    escValue      = 1520;
  }
  
  steeringValue = 135 - incomingInt.toInt();
  //Serial.print(steeringValue);
  //Serial.print("--");
  //Serial.println(incomingInt.toInt());
  
//  if ( incomingInt.toInt() > 0 && incomingInt.toInt() < 100 ) {
//    Serial.println("Less than 100");
//  } else {
//    Serial.println( incomingInt.toInt() );
//  }
  
  delay(00);
}

void calculateRightDistance() {
  digitalWrite(triggerRight, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerRight, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerRight, LOW);

  durationRight = pulseIn(echoRight, HIGH);
  distanceRight = durationRight * 0.034/2;
  
  Serial.println(distanceRight);
}

void calculateLeftDistance() {
  digitalWrite(triggerLeft, LOW);
  delayMicroseconds(2);
  digitalWrite(triggerLeft, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerLeft, LOW);

  durationLeft = pulseIn(echoLeft, HIGH);
  distanceLeft = durationLeft * 0.034/2;
}
