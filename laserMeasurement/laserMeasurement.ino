 
int dir = 9;
int Step = 8;
int homePin = 2;
int motorSpeed = 0;
int homeSpeed = 2000;
int runProgramSpeed = 2500;
int runPartHomeSpeed = 1000;
int startPos, endPos, tempPos = 0;
int pos = 0; // calulate base on number of pulse from driver
bool is_fw, is_run, is_home, is_jog, is_runProgram, is_runPartHome= false;
String msg = "";
String jogDirection = "";

void readSerialPort() {
 //Read the command which is sent from raspberry
 msg = "";
 if (Serial.available()) {
   delay(10);
   while (Serial.available() > 0) {
     msg += (char)Serial.read();
   }
   Serial.flush();
 }
}

void runMotor(int mSpeed){
  // Run the motor clockwise or counter clockwise after reading the
  // command from raspberry
  if (is_run == true){
    if (is_fw == true){
      digitalWrite(dir, HIGH);
    }else{
      digitalWrite(dir, LOW);
    }
  
    digitalWrite(Step, HIGH);
    delayMicroseconds(motorSpeed);
    digitalWrite(Step, LOW);
    delayMicroseconds(motorSpeed);
}
  
}

void runProgram(){
  if (is_runProgram == true){
    if (startPos < endPos){
      digitalWrite(dir, HIGH);
      tempPos = endPos;
    }else{
      digitalWrite(dir, LOW);
      // swap startPos and endPos to make startPos less than endPos
      tempPos = endPos;
      endPos = startPos;
      startPos = tempPos;
      
    }
    
//    Serial.print("Start Pos: "); Serial.println(startPos);
//    Serial.print("End Pos: "); Serial.println(endPos);
    delay(2000);
    for (int i=startPos; i<endPos; i++){
      digitalWrite(Step, HIGH);
      delayMicroseconds(runProgramSpeed);
      digitalWrite(Step, LOW);
      delayMicroseconds(runProgramSpeed);
    }
    delay(2000);
    Serial.println("s");//Send signal to raspberry to send another position
    is_runProgram = false;
    // Set start position to end position so that the end position can be updated
    //to a new value from dataPos list from raspberry
    startPos = tempPos;  
//    Serial.print("Start Pos after stop: "); Serial.println(startPos);
  }
}

void runPartHome(){
  // After finish running program then need to be turn back to part home position
  if (is_runPartHome == true){
    digitalWrite(dir, LOW);
    for (int i=0; i<endPos; i++){
      digitalWrite(Step, HIGH);
      delayMicroseconds(runPartHomeSpeed);
      digitalWrite(Step, LOW);
      delayMicroseconds(runPartHomeSpeed);
  // Turn off runPartHome and reset stat position to zero
      if ( i == (endPos - 1)){
        is_runPartHome = false;
        startPos = 0;
        Serial.println("d"); // Done runPartHome
      }
      
    } 
  }
}

void homeMachine(){
  while (is_home == true){
    digitalWrite(dir, LOW);
    digitalWrite(Step, HIGH);
    delayMicroseconds(homeSpeed);
    digitalWrite(Step, LOW);
    delayMicroseconds(homeSpeed);
    
  }
  
}

void myHome(){
  is_home = false;
  pos = 0;
  Serial.println(pos);
}

void jogMachine(String jog_dir){
  if (jog_dir == "fw"){
    digitalWrite(dir, HIGH);
  }
  if (jog_dir == "bw"){
    digitalWrite(dir, LOW);
  }
  if (is_jog == true){
    digitalWrite(Step, HIGH);
    delayMicroseconds(homeSpeed);
    digitalWrite(Step, LOW);
    delayMicroseconds(homeSpeed);
    if(jog_dir == "fw"){
      pos++;
    }else{
      pos-- ;
    }
    
  }
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(dir, OUTPUT);
  pinMode(Step, OUTPUT);
  pinMode(homePin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(homePin), myHome, FALLING);
  
}

void loop() {
  // put your main code here, to run repeatedly:
  readSerialPort();
  if (msg != "")
  {
    char val = msg.charAt(0);
    motorSpeed = msg.substring(1, msg.length()).toInt();
    //Serial.println(motorSpeed);
    switch(val){
      case('o'):
        is_run = true;
        is_fw = true;
        break;
       case('f'):
        is_run = true;
        is_fw = false;
        break;
      case('q'):
        is_run = false;
        break; 
      case('h'):
        is_home = true;
        break; 
      case('j'):
        is_jog = true;
        jogDirection = "fw";
        break;
      case('k'):
        is_jog = true;
        jogDirection = "bw";
        break;
      case('m'):
        is_runPartHome = true;
        break;
      case('n'):
        is_jog = false;
        Serial.println(pos);
        break;
      case('p'):
        is_runProgram = true;
        endPos = motorSpeed;
        break;  
      case('a'):
        startPos = 0;
        pos = 0;
        Serial.println("a");
        break; 
      case('b'):
        endPos = pos;
        is_runPartHome = true;
        break;            
      }
    }
    
    runMotor(motorSpeed);
    homeMachine();
    jogMachine(jogDirection);
    runProgram();
    runPartHome();
    

}
