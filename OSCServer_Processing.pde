import processing.net.*;
import oscP5.*;
import netP5.*;

//Declare the variables
float position;
OscP5 oscP5;
NetAddress myRemoteLocation;
//float OSCvalue;
String OSCvalue;
String val;

void setup() {
 size(400,400);
 /* start oscP5, listening for incoming messages at port 12000 */
 oscP5 = new OscP5(this,12000);
 //NetAddress takes two parameters - IP address and a port number
 myRemoteLocation = new NetAddress("localhost",12000);
}


void oscEvent(OscMessage theOscMessage) {
  //check if theOscMessage has the address pattern we are looking for.
  if(theOscMessage.checkAddrPattern("/address") == true) {
    //get the first value of the messafe reseived and convert it into String
      OSCvalue = theOscMessage.get(0).stringValue(); 
      //print out the value in the console
      println(OSCvalue);
      //if statements which check if the value received is either 'pos' or 'neg'
      //and sets the val to a string which is either 'pos' or 'neg'
      if(OSCvalue.equals("pos")){
       val = "pos";
      }
       else if(OSCvalue.equals("neg")){
       val = "neg";
      }
  }
}
//if the value is positive, based on the frame rate change the random red value
//so the background returns warm colours
void draw(){
if(val=="pos") {
  frameRate(0.5);
  for(int i=0; i<frameRate; i++){
  background(random(120,255), 100, 100);
  }
//if the val is negative, return cold colours
}else if (val=="neg") {
  frameRate(1.5);
  for(int i=0; i<frameRate; i++){
  background(100, random(120,255), random(100,200));
  }
}
}
