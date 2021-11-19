import java.net.*;
import java.io.*;

public class EchoServer
{
   public static void main (String[] args) throws IOException
   {
      if (args.length != 1)
      {
         System.err.println ("Usage: java EchoServer <port number>");
         System.exit (1);
      }

      int portNumber, clientCounter = 1;

      try
      {
         portNumber = Integer.parseInt(args[0]);
      }
      catch (NumberFormatException e)
      {
         portNumber = 58888;
      }

      try
      (
         ServerSocket serverSocket = new ServerSocket (portNumber);
      )
      {
         while (true)
         {
            System.out.println ("\nListening for client connections on port: " + portNumber + "... ");
            new EchoServerThread ("client-" + clientCounter, serverSocket.accept()).start();
            System.out.println ("Client #" + clientCounter + " joined");
            clientCounter++;
         }
      }
      catch (IOException e)
      {
         System.out.println ("Exception caught when trying to listen on port " + portNumber + " or listening for a connection");
         System.out.println (e.getMessage());
      }
   }
}
