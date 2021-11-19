import java.net.*;
import java.io.*;
import java.util.*;
import java.nio.charset.*;

public class EchoClient
{
   public static void main (String[] args) throws IOException
   {
      if (args.length != 6)
      {
         System.err.println ("Usage: java EchoClient <host name> <port number> <measurement type> <number of probes> <message size> <server delay>");
         System.err.println ("\tMeasurement type: rtt - round trip time, tput - throughput");
         System.err.println ("\tMessage size for RTT: 1, 100, 200, 400, 800, 1000 bytes");
         System.err.println ("\tMessage size for throughput: 1024, 2048, 4096, 8192, 16384, 32768 bytes");
         System.exit(1);
      }

      String hostName = args[0];
      int numberProbes, messageSize, serverDelay, portNumber;

      try
      {
         portNumber = Integer.parseInt(args[1]);
      }
      catch (NumberFormatException e)
      {
         portNumber = 58888;
      }

      String measurementType = args[2];

      if (!measurementType.equals ("rtt") && !measurementType.equals ("tput"))
         measurementType = "rtt";

      try
      {
         numberProbes = Integer.parseInt(args[3]);
      }
      catch (NumberFormatException e)
      {
         numberProbes = 10;
      }

      if (numberProbes < 10)
         numberProbes = 10;

      try
      {
         messageSize = Integer.parseInt(args[4]);
      }
      catch (NumberFormatException e)
      {
         messageSize = 100;
      }

      try
      {
         serverDelay = Integer.parseInt (args[5]);
      }
      catch (NumberFormatException e)
      {
         serverDelay = 0;
      }

      System.out.println ("\nConnecting to host " + hostName + " on port " + portNumber + " ...");

      try
      (
         Socket socket = new Socket (hostName, portNumber);
         OutputStream socketOut = socket.getOutputStream();
         InputStream socketIn = socket.getInputStream();
      )
      {
         System.out.println ("Successfully connected");
         System.out.println ("\nCommencing CSP...");

         String messageOut, messageIn = "";
         char charRead = ' ';
         long[] probeTimes = new long[numberProbes];
         long probeStart, probeEnd, probeTime;

         // <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n
         messageOut = "s " + measurementType + " " + numberProbes + " " + messageSize + " " + serverDelay + "\n";
         socketOut.write (messageOut.getBytes (StandardCharsets.US_ASCII));
         socketOut.flush();

         while (charRead != '\n')
         {
            charRead = (char) socketIn.read();
            messageIn += charRead;
         }

         System.out.println ("Sent CSP request to the server: \'" + messageOut.substring (0, messageOut.length() - 1) + "\\n\'");
         System.out.println ("Received CSP response from the server: \'" + messageIn.substring (0, messageIn.length() - 1) + "\\n\'");

         switch (messageIn)
         {
            default:
               System.err.println ("Invalid response received from the server during CSP. Aborting ...");
               System.exit(1);

            case "404 ERROR: Invalid Connection Setup Message\n":
               System.err.println ("Error received from the server during CSP. Aborting ...");
               System.exit(1);

            case "200 OK: Ready\n":
               System.out.println ("CSP completed successfully");
               System.out.print ("\nCommencing MP...");

               String payload = "0".repeat(messageSize);

               for (int i = 1; i <= numberProbes; i++)
               {
                  // <PROTOCOL PHASE><WS><PROBE SEQUENCE NUMBER><WS><PAYLOAD>\n

                  messageOut = "m " + i + " " + payload + "\n";
                  messageIn = "";
                  charRead = ' ';

                  // Beginning of the experiment
                  probeStart = System.currentTimeMillis();
                  socketOut.write (messageOut.getBytes(StandardCharsets.US_ASCII));
                  socketOut.flush();

                  while (charRead != '\n')
                  {
                     charRead = (char) socketIn.read();
                     messageIn += charRead;
                  }
                  probeEnd = System.currentTimeMillis();
//System.out.println ("messageOut = " + messageOut);
//System.out.println ("messageIn = " + messageIn);
                  // End of the experiment

                  System.out.println ("\nSent MP probe " + i + "/" + numberProbes + " to the server: \'m " + i + " <payload omitted>\\n\'");
                  System.out.println ("Received MP response from the server: \'m " + i + " <payload omitted>\\n\'");

                  if (messageIn.equals ("404 ERROR: Invalid Measurement Message\n"))
                  {
                     System.err.println ("Error received from the server during MP. Aborting...");
                     System.exit(1);
                  }
                  else
                  {
                     System.out.println ("Probe successfully received by the server");
                     probeTime = probeEnd - probeStart;
                     System.out.println ("RTT for this probe was: " + probeTime + "ms");
                     System.out.println ("Saving result...");
                     probeTimes[i-1] = probeTime;
                  }
               }

               System.out.println ("MP completed successfully");
               //System.out.println ("Writing data to disk ...");
               System.out.println ("\nCommencing CTP...");

               messageOut = "t\n";
               messageIn = "";
               charRead = ' ';

               socketOut.write (messageOut.getBytes(StandardCharsets.US_ASCII));
               socketOut.flush();
               System.out.println ("Sent CTP request to the server:  \'t\\n\'");

               while (charRead != '\n')
               {
                  charRead = (char) socketIn.read();
                  messageIn += charRead;
               }

               System.out.println ("Received CTP response from the server: \'" + messageIn.substring(0, messageIn.length() - 1) + "\\n\'");

               switch (messageIn)
               {
                  default:
                     System.err.println ("Invalid response received from the server during CTP. Aborting...");
                     System.exit(1);

                  case "404 ERROR: Invalid Connection Termination Message\n":
                     System.err.println ("Error received from the server during CTP. Aborting...");
                     System.exit(1);

                  case "200 OK: Closing Connection\n":
                     System.out.println ("CTP completed successfully\n");
                     System.out.println ("Writing results of the experiments to disk...\n");

                     String plotFileName, fileOutput;

                     if (measurementType.equals ("rtt"))
                     {
                        plotFileName = "plot_rtt.dat";
                        long result = 0;

                        for (int i = 0; i < numberProbes; i++)
                           result += probeTimes[i];

                        fileOutput = messageSize + " " + ((double) result / numberProbes);
                     }
                     else // "tput"
                     {
                        plotFileName = "plot_tput.dat";
                        double result = 0.0;

                        for (int i = 0; i < numberProbes; i++)
                           result = (double) messageSize / probeTimes[i];

                        fileOutput = messageSize + " " + (result / numberProbes);
                     }

                     try
                     (
                        FileWriter fw = new FileWriter (plotFileName, true); // true means append to the end of the file
                        PrintWriter fileOut = new PrintWriter (fw, true); // true means auto-flush the buffer
                     )
                     {
                        fileOut.println (fileOutput);
                        //fileOut.printf("%.3f", valueRounded);
                     }
                     catch (FileNotFoundException e)
                     {
                        System.err.println ("Output file " + plotFileName + " not found");
                     }

                     System.out.println ("Exiting gracefully...");
                     System.exit(0);
               }
         }
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


/*
         System.out.println ("Encoded text: \'" + messageOut + "\'");
         socketOutBytes.write (messageOutBytes);
         socketOutBytes.flush();
         System.out.println ("Encoded bytes: \'" + Arrays.toString (messageOutBytes) + "\'");
         byte[] messageOutBytes;
         byte[] messageOut = new byte[15];
         ArrayList bytesArray = new ArrayList();

         bytesArray.add ("s ");
         bytesArray.add (measurementType);
         bytesArray.add (" ");
         bytesArray.add (numberProbes);
         bytesArray.add (" ");
         bytesArray.add (messageSize);
         bytesArray.add (" ");
         bytesArray.add (serverDelay);
         bytesArray.add ("\n");

         //messageOutBytes = bytesArray.toArray (new Byte());
//[115, 32, 114, 116, 116, 32, 49, 48, 32, 49, 32, 48, 10]
         messageOutBytes[0] = 115;
         messageOutBytes[1] = 32;
         messageOutBytes[2] = 114;
         messageOutBytes[3] = 116;
         messageOutBytes[4] = 116;
         messageOutBytes[5] = 32;

         System.out.println ("Encoded text: \'" + messageOutText + "\'");
         System.out.println ("Encoded bytes: \'" + Arrays.toString (messageOutBytes) + "\'");
         socketOutBytes.write (messageOutBytes);
         socketOutBytes.flush();

//         System.out.println ("Measurement protocol message format: ");
//         System.out.println ("\t<PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>\n");
//         System.out.print ("\nEnter a message to send to the server: ");
//         userInput = keyboardIn.readLine();
//         messageOutText = ("s " + measurementType + " ");
         //messageOutBytes = messageOutText.getBytes(StandardCharsets.US_ASCII);
         //messageOutBytes.add (numberProbes);
//         messageOutBytes.add


         System.out.println ("Sent CSP request to the server: \'" + messageOutText + "\'");
         System.out.println ("Encoded text: \'" + messageOutText + "\'");
         System.out.println ("Encoded bytes: " + Arrays.toString (messageOutBytes));
         byte[] messageOut = new byte[15];
         messageOut[0] = 115;
         messageOut[1] = 32;
         messageOut[2] = ;
         messageOut[3] = ;
         messageOut[4] = ;


         //socketOutText.println (messageOutText);
//         String strCurrentLine;
         // socketOut.flush(); - no longer needed becasue auto-flush is set to true
         //System.out.println ("Message sent to the server: " + messageOut);
//         while ((strCurrentLine = socketIn.readLine()) != null)
 //        {
   //         System.out.println(strCurrentLine);
     //    }
//System.out.println(socketIn.ready());
//System.out.println(socketIn.ready());


               // Arrays.fill (new byte[messageSize], (byte) 8);
               //byte[] messageOutBytes = new byte[messageSize + 5];




                  //messageOutBytes = "m " + i + " " + payload + "\n";

                  messageOutBytes[0] = 109;
                  messageOutBytes[1] = 32;
                  messageOutBytes[2] = 105;
                  messageOutBytes[3] = 32;
                  messageOutBytes[messageSize + 4] = 10;

                  //ba = new String ("m " + i + " ").getBytes();
                  //newLine = "\n".getBytes();


System.out.println ("messageOuttext = " + messageOutText);
                 // socketOutBytes.writeBytes (messageOutText);
System.out.println ("after socket.outtext.println");
System.out.println (socketIn.readLine());
//                  socketOutText.flush();
                  //socketOutBytes.write (messageOutBytes);
                  //socketOutBytes.flush ();
//int avail = 1;
//avail = socketInBytes.available();
//System.out.println ("bytes available: " + avail);
//byte[] buf = new byte[avail];
//socketInBytes.readFully(buf);
//System.out.println ("bytes read: " + buf);
//System.out.println (socketIn.ready());
//                  int essageIn = socketIn.read();
//                  ArrayList buf = new ArrayList();

//                  while ((essageIn = socketIn.read()) != -1)
  //                   buf.add(essageIn);
//System.out.println ("after socketin.println");
//                  StringBuilder sb = new StringBuilder();
 //                 for (int j = buf.size() - 1; j >= 0; j--) {
  //                  int num = (int) buf.get(j);
   //                 sb.append(num);
    //              }
      //            messageIn = sb.toString();
*/
