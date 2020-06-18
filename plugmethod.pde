import oscP5.*;
import netP5.*;

OscP5 osc;
NetAddress remote;

void setup() {
  size( 400, 400 );
  
  /* start oscP5, and listen on port 12000 */
  osc = new OscP5( this, 12000 );
  
  /* our remote address here will point to 'osc' of this sketch */
  remote = new NetAddress( "127.0.0.1", 12000 );
  
  
  /* plug a function of your sketch to an address-pattern and typetag of
   * an OscMessage you are expecting, the arguments will then be forwarded to
   * the corresponding function inside your sketch.
   * 1. argument: an object, here a reference to this sketch
   * 2. argument: a String, the name of a function 
   * 3. argument: an address-pattern
   * 4. argument: a typetag 
   */
  osc.plug(this, "test", "/test" , "ii");
}

void test(int a, int b ) {
  println("hello "+ a + ", " + b );
}

void draw() {
}

/* send some test message on keyPressed */
void keyPressed() {
    OscMessage m = new OscMessage("/test");
    m.add(1);
    m.add(2);
    osc.send( m , remote ); 
}
