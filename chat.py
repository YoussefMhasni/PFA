import random
import json
import re
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from function import Gsearch, stocks, news1,news2
#selenium

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

    
FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
#===================================Functions
import warnings
warnings.filterwarnings('ignore')
#------------------------------------------------------------------
#==================================================================
bot_name = "Sam"
clientstag=["balance","deposit","spending","transfer"]
def searching(query,x):
        with open('user.json', 'r') as jsn_data:
            inte = json.load(jsn_data)
        phrases=[]
        sentence = tokenize(query.lower())
        X = bag_of_words(sentence, all_words)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(device)

        output = model(X)
        _, predicted = torch.max(output, dim=1)

        tag = tags[predicted.item()]

        probs = torch.softmax(output, dim=1)
        prob = probs[0][predicted.item()]
        if prob.item() > 0.75:
            for intent in intents['intents']:
                if tag == intent["tag"]:
                    if(tag=="Stocks"):
                     return stocks(query)
                    elif(tag=="news1"):
                        list1=news1()
                        return list1[0].text                    
                    elif(tag=="news2"):
                        list2=news2()
                        return list2[0].text
                    elif(tag=="Informations") :
                        for elem in intent['patterns']:
                            phrases.extend(tokenize(elem.lower()))
                            for i in list(sentence):
                                if i in phrases:
                                    sentence.remove(i)
                        return Gsearch(query," ".join(sentence))    
                    elif tag in clientstag:
                        if (x==True):
                                #if user is authentificated:
                                if(tag=="balance"):
                                  return  random.choice(intent['responses'])+" "+ str(inte['solde'])
                                elif(tag=="deposit"):
                                    return  random.choice(intent['responses'])
                                elif(tag=="spending"):
                                    return  random.choice(intent['responses'])
                                elif(tag=="transfer"):
                                    return  random.choice(intent['responses'])+" "+str(inte['transfer_date'])+", the amount transfered was : "+str(inte['transfer_amount'])+" Dh, in favour of "+str(inte['transfer_destinataire'])
                                else:
                                    return "Im sorry, i didnt understand"
                        else:
                            return 'Connect to Your account first! ' 
                    else:
                        return  random.choice(intent['responses']) 
        else: 
            return " I do not understand..."
