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

      int portNumber = Integer.parseInt (args[0]);
      int clientCounter = 1;

      try
      (
         ServerSocket serverSocket = new ServerSocket (portNumber);
      )
      {
         while (true)
         {
            System.out.println ("\nListening for client connections on port: " + portNumber + " ... ");

            Socket clientSocket = serverSocket.accept();
            System.out.println ("Client #" + clientCounter + " joined");

            BufferedReader socketIn = new BufferedReader (new InputStreamReader (clientSocket.getInputStream()));
            PrintWriter socketOut = new PrintWriter (clientSocket.getOutputStream(), true); // true means auto-flush

            String messageIn = socketIn.readLine();
            System.out.println ("Message received from the client: " + messageIn);

            socketOut.println (messageIn);
            System.out.println ("Message sent to the client: " + messageIn);

            clientSocket.close();
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
