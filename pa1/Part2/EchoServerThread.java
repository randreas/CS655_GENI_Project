
import java.net.*;
import java.io.*;
import java.nio.charset.*;

public class EchoServerThread extends Thread
{
   private Socket socket = null;
   private String threadName;
   private boolean endThread = false;

   public EchoServerThread (String threadName, Socket socket)
   {
      super (threadName);
      this.threadName = threadName;
      this.socket = socket;
   }

   public void run()
   {
      try
      (
         OutputStream socketOut = socket.getOutputStream();
         InputStream socketIn = socket.getInputStream();
         //BufferedReader socketIn = new BufferedReader (new InputStreamReader (clientSocket.getInputStream()));
         //PrintWriter socketOut = new PrintWriter (clientSocket.getOutputStream(), true); // true means auto-flush
      )
      {
         System.out.println ("\nThread: " + threadName + ". Commencing CSP...");

         // <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n

         String messageOut = "200 OK: Ready\n", messageIn = "", measurementType;
         char charRead = ' ';
         String[] msgVars;
         int numberProbes = 0, messageSize = 0, serverDelay = 0;

         while (charRead != '\n')
         {
            charRead = (char) socketIn.read();
            messageIn += charRead;
         }

         messageIn = messageIn.substring (0, messageIn.length() - 1);

         System.out.println ("Thread: " + threadName + ". Received CSP request from the client: \'" + messageIn + "\\n\'");
         System.out.println ("Thread: " + threadName + ". Checking CSP request format...");

         //messageOut = "s " + measurementType + " " + numberProbes + " " + messageSize + " " + serverDelay + "\n";
         msgVars = messageIn.split (" ");

         try
         {
            numberProbes = Integer.parseInt(msgVars[2]);
            messageSize = Integer.parseInt(msgVars[3]);
            serverDelay = Integer.parseInt(msgVars[4]);

            if (!msgVars[0].equals ("s") || (!msgVars[1].equals ("rtt") && !msgVars[1].equals ("tput")) || numberProbes < 1 || messageSize < 1 || serverDelay < 0)
               throw new Exception ("Thread: " + threadName + ". Invalid CSP request");
         }
         catch (Exception e)
         {
            messageOut = "404 ERROR: Invalid Connection Setup Message\n";
            socketOut.write (messageOut.getBytes (StandardCharsets.US_ASCII));
            socketOut.flush();
            System.err.println ("Thread: " + threadName + ". Received invalid CSP request. Aborting...");
            socket.close();
            this.stop();
         }

         measurementType = msgVars[1];

         //"200 OK: Ready"
         //"404 ERROR: Invalid Connection Setup Message"

//         System.out.println ("Logging values of variables...");

         System.out.println ("Thread: " + threadName + ". Validated CSP request format");

         socketOut.write (messageOut.getBytes (StandardCharsets.US_ASCII));
         socketOut.flush();

         System.out.println ("Thread: " + threadName + ". Sent CSP response to the client: \'" + messageOut.substring (0, messageOut.length() - 1) + "\\n\'");
         System.out.println ("Thread: " + threadName + ". CSP completed successfully");

         System.out.println ("\nThread: " + threadName + ". Commencing MP...");

         int probeCounter = 1, probeNumber = 0;

         while (true)
         {
            // <PROTOCOL PHASE><WS><PROBE SEQUENCE NUMBER><WS><PAYLOAD>\n
            messageIn = "";
            charRead = ' ';
            probeNumber = 0;

            while (charRead != '\n')
            {
               charRead = (char) socketIn.read();
               messageIn += charRead;
            }

            System.out.println ("\nThread: " + threadName + ". Received MP probe #" + probeCounter + " from the client");
            System.out.println ("Thread: " + threadName + ". There should be additional " + (numberProbes - probeCounter) + " MP probes coming... #");
            System.out.println ("Thread: " + threadName + ". Checking MP probe format...");

            msgVars = messageIn.substring (0, messageIn.length() - 1).split (" ");

            try
            {
               probeNumber = Integer.parseInt(msgVars[1]);
               //payload = msgVars[2];

               if (!msgVars[0].equals ("m") || probeNumber != probeCounter || msgVars[2].length() != messageSize)
                  throw new Exception ("Thread: " + threadName + ". Invalid MP probe");
            }

            catch (Exception e)
            {
               messageOut = "404 ERROR: Invalid Measurement Message\n";
               socketOut.write (messageOut.getBytes (StandardCharsets.US_ASCII));
               socketOut.flush();
               System.err.println ("Thread: " + threadName + ". Received invalid MP probe. Aborting...");
               socket.close();
               this.stop();
            }

            System.out.println ("Thread: " + threadName + ". Validated MP probe format");

            Thread.sleep (serverDelay);

            socketOut.write (messageIn.getBytes (StandardCharsets.US_ASCII));
            socketOut.flush();

            System.out.println ("Thread: " + threadName + ". Echoed MP probe to the client: \'" + messageIn.substring (0, messageOut.length() - 1) + "\\n\'");
System.out.println("probeNumber = " + probeNumber);
System.out.println("probeCounter = " + probeCounter);
            if (probeNumber == numberProbes)
               break;

            probeCounter++;
         }

         System.out.println ("Thread: " + threadName + ". MP completed successfully");
         System.out.println ("\nThread: " + threadName + ". Commencing CTP...");

         messageOut = "200 OK: Closing Connection\n";
         messageIn = "";
         charRead = ' ';

         while (charRead != '\n')
         {
            charRead = (char) socketIn.read();
            messageIn += charRead;
         }

         messageIn = messageIn.substring(0, messageIn.length() - 1);

         System.out.println ("Thread: " + threadName + ". Received CTP request from the client: \'" + messageIn + "\\n\'");
         System.out.println ("Thread: " + threadName + ". Checking CTP request format...");

         try
         {
            if (!messageIn.equals ("t"))
               throw new Exception ("Thread: " + threadName + ". Invalid CTP request");
         }

         catch (Exception e)
         {
            messageOut = "404 ERROR: Invalid Connection Termination Message\n";
            socketOut.write (messageOut.getBytes (StandardCharsets.US_ASCII));
            socketOut.flush();
            System.err.println ("Thread: " + threadName + ". Received invalid CTP request. Aborting...");
            socket.close();
            this.stop();
         }

         System.out.println ("Thread: " + threadName + ". Validated CTP request format");

         socketOut.write (messageOut.getBytes (StandardCharsets.US_ASCII));
         socketOut.flush();

         System.out.println ("Thread: " + threadName + ". Sent CTP response to the client: \'" + messageOut.substring (0, messageOut.length() - 1) + "\\n\'");
         System.out.println ("Thread: " + threadName + ". CTP completed successfully\n");
         System.out.println ("Thread: " + threadName + ". Exiting gracefully...");
         socket.close();
         this.stop();
      }

      catch (Exception e)
      {
         e.printStackTrace();
      }
   }
}
