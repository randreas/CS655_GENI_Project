import math
        

class SampleStatistics:
    def __init__(self):
        self.std_dev =0.0
        self.__total_sum= 0
        self.count = 0
        self.min = None
        self.max = None

    def add(self,sample):
        if self.count > 0:
            self.__updateSTD_Dev(sample)
            self.__updateMinMax(sample)

        else:
            self.__total_sum = sample
            self.count = self.count + 1
            self.min = sample
            self.max = sample
        
    def __updateMinMax(self,sample):
        if sample < self.min:
                self.min = sample
        if sample > self.max:
                self.max = sample
        
    def __updateSTD_Dev(self,sample):
        #This is an online STD dev calculator
        #It uses an estimation of the STD deviation instead of recalcutating
        #the whole standard Dev using least squares for each new incoming sample
        #the trade off is that it can be less acurate the traditional STD deviation calcuation
        oldMean = self.getMean()

        self.__total_sum = self.__total_sum + sample
        self.count = self.count +1
        newMean = self.getMean()

        self.std_dev = math.sqrt( (( (self.count-1)*pow(self.std_dev,2.0) + (sample-newMean)*(sample-oldMean))) / self.count)
    
    def getMean(self):
        return self.__total_sum / self.count
            


class ServerObserver:
    def __init__(self):
        self.latency = SampleStatistics()
        self.throughput = SampleStatistics()
