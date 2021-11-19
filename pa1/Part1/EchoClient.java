import java.net.*;
import java.io.*;

public class EchoClient
{
   public static void main (String[] args) throws IOException
   {
      if (args.length != 2)
      {
         System.err.println ("Usage: java EchoClient <host name> <port number>");
         System.exit(1);
      }

      String hostName = args[0];
      int portNumber = Integer.parseInt(args[1]);

      try
      (
         Socket socket = new Socket (hostName, portNumber);
         // true means auto-flush the buffer after every write to the stream
         BufferedReader socketIn = new BufferedReader (new InputStreamReader (socket.getInputStream()));
         PrintWriter socketOut = new PrintWriter (socket.getOutputStream(), true);
         BufferedReader keyboardIn = new BufferedReader (new InputStreamReader (System.in))
      )
      {
         String userInput, messageOut, messageIn;

         System.out.print ("Enter a message to send to the server: ");
         userInput = keyboardIn.readLine();

         messageOut = userInput;
         socketOut.println (messageOut);
         // socketOut.flush(); - no longer needed becasue auto-flush is set to true
         System.out.println ("Message sent to the server: " + messageOut);

         messageIn = socketIn.readLine();
         System.out.println ("Message received from the server: " + messageIn);
      }
      catch (UnknownHostException e)
      {
         System.err.println("Don't know about host " + hostName);
         System.exit(1);
      }
      catch (IOException e)
      {
         System.err.println("Couldn't get I/O for the connection to " + hostName);
         System.exit(1);
      }
   }
}
