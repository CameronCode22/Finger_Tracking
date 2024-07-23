#define LEND1 2  // Thumb
#define LEND2 3  // Index
#define LEND3 4  // Middle
#define LEND4 5  // Ring
#define LEND5 6  // Little

void setup() {
  pinMode(LEND1, OUTPUT);
  pinMode(LEND2, OUTPUT);
  pinMode(LEND3, OUTPUT);
  pinMode(LEND4, OUTPUT);
  pinMode(LEND5, OUTPUT);

  Serial.begin(9600);
  Serial.println("Ready");
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');  // Read the incoming string
    Serial.print("Command received: ");
    Serial.println(command);

    // Ensure the command length is 5 (for 5 LEDs)
    if (command.length() == 5) {
      // Parse and set LED states based on the command string
      digitalWrite(LEND1, command[0] == '1' ? HIGH : LOW);
      digitalWrite(LEND2, command[1] == '1' ? HIGH : LOW);
      digitalWrite(LEND3, command[2] == '1' ? HIGH : LOW);
      digitalWrite(LEND4, command[3] == '1' ? HIGH : LOW);
      digitalWrite(LEND5, command[4] == '1' ? HIGH : LOW);
    }
  }

  delay(100);
}
