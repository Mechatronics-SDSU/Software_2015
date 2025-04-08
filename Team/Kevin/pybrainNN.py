'''
Created on Feb 7, 2015

@author: kevin
'''
import cv2
import pybrain
import pybrain.datasets as datasets
import pybrain.supervised.trainers as trainers


network = pybrain.FeedForwardNetwork()


def Train(epocs):
    
    rawImg1 = cv2.imread('C:\Users\kevin\Pictures\Hammer.jpg',0)
    h, w =  rawImg1.shape
    print rawImg1.shape

    print rawImg1[0]
    
    Dataset = datasets.SupervisedDataSet(315, 1)
    for x in range(0, h):
        Dataset.addSample(rawImg1[x], 1)
    
    
    inLayer = pybrain.LinearLayer(315)
    hiddenLayer = pybrain.SigmoidLayer(20)
    outLayer = pybrain.SoftmaxLayer(1) #Softmax gives probabilities
    
    network.addInputModule(inLayer)
    network.addModule(hiddenLayer)
    network.addOutputModule(outLayer)
    
    in_to_hidden = pybrain.FullConnection(inLayer, hiddenLayer)
    hidden_to_out = pybrain.FullConnection(hiddenLayer, outLayer)
    network.addConnection(in_to_hidden)
    network.addConnection(hidden_to_out)
    
    network.sortModules()
    
    T = trainers.BackpropTrainer(network, learningrate = 0.09, momentum = 0.9)
    #print 'Error Before:', T.testOnData(Dataset, True)
    T.trainOnDataset(Dataset, epocs)
    #print '\nError After:', T.testOnData(Dataset, True)
   
    k=0 
    for y in range(0, h):
        k= network.activate(rawImg1[y]) +k
   
    print k
    #print network.activate(rawImg1[0]) 


if __name__ == "__main__":      
    Train(100)
    
   