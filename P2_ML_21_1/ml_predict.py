import pickle


def predict(Xdata):
    
    loaded_model, loaded_scaler = pickle.load( open('RFC_86.37_SC_200214_053559.pkl', 'rb') )
    
    Xdata = loaded_scaler.transform(Xdata)
    
    result = loaded_model.predict(Xdata)
    
    return result