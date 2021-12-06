import sys, getopt


# python .\mainFile.py -c 1 -o txt -l 5
def main(argv):
   cacheUse = ''
   percLoss = ''
   objFile = ''

   try:
      opts, args = getopt.getopt(argv,"hc:o:l:",["c=","object=","percLoss"])
   except getopt.GetoptError:
      
      print('mainFile.py -c <1/0> -o <objectFile> -l <percentageLoss>')
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print('mainFile.py -c <1/0> -o <objectFile> -l <percentageLoss>')
         print('-c <1/0> 1 for cache 0 for no cache')
         print('-l <percentageLoss> (0-100)')
         sys.exit()
      elif opt in ("-c", "--cache"):
         cacheUse = arg
      elif opt in ("-o", "--object"):
         objFile = arg
      elif opt in ("-l", "--percLoss"):
         percLoss = arg



   print('Cache in use ', cacheUse)
   print('Object file is ', objFile)
   print('Percentage Loss is ', percLoss)

if __name__ == "__main__":
   main(sys.argv[1:])