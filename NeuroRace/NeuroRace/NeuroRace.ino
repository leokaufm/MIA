#include <ESP8266WiFi.h>
#include <WiFiUdp.h>

#define ENA D3  // Speed control for Motor A
#define ENB D2  // Speed control for Motor B

#define MOTORB_1 D4 // izquierda
#define MOTORB_2 D5
#define MOTORA_1 D7 // derecha
#define MOTORA_2 D6

// WiFi credentials
const char* ssid = "RouterBrainware";
const char* password = "!Brainware@451";

// UDP settings
WiFiUDP udp;
const unsigned int localUdpPort = 4210; // Port to listen on
char incomingPacket[255]; // Buffer for incoming packets

// Threshold to trigger the motor
const int threshold = 50;

void setup() {
  delay(5000);
  Serial.begin(115200);
  Serial.println();

  WiFi.begin(ssid, password);
  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected, IP address: ");
  Serial.println(WiFi.localIP());

  // Start UDP
  udp.begin(localUdpPort);
  Serial.printf("UDP listening on IP: %s, port: %d\n", WiFi.localIP().toString().c_str(), localUdpPort);

  // Configuration des pins en sortie
  Serial.print("Configuration des pins en sortie");
  pinMode(MOTORA_1, OUTPUT);
  pinMode(MOTORA_2, OUTPUT);

  pinMode(MOTORB_1, OUTPUT);
  pinMode(MOTORB_2, OUTPUT);

  pinMode(ENA, OUTPUT);
  pinMode(ENB, OUTPUT);

}

void loop() {
  int packetSize = udp.parsePacket();
  if (packetSize) {
    // receive incoming UDP packet
    int len = udp.read(incomingPacket, 255);
    if (len > 0) {
      incomingPacket[len] = 0;
    }

    Serial.printf("Received UDP packet: %s\n", incomingPacket);

    // Convert to integer
    int receivedValue = atoi(incomingPacket);

    // Do something with the value
    if (receivedValue == 1) {
      Serial.println("Threshold reached, starting motor...");
      // Initialiser la direction des moteurs
      Serial.print("Initialiser la direction des moteurs\n");
      digitalWrite(MOTORA_1, HIGH);
      digitalWrite(MOTORA_2, LOW);
      digitalWrite(MOTORB_1, LOW);
      digitalWrite(MOTORB_2, HIGH);

      // Set motor speed (0-1023 on ESP8266)
      analogWrite(ENA, 200);
      analogWrite(ENB, 200);
    } else {
      digitalWrite(MOTORA_1, LOW);
      digitalWrite(MOTORA_2, LOW);
      digitalWrite(MOTORB_1, LOW);
      digitalWrite(MOTORB_2, LOW); 
    }
  }
}