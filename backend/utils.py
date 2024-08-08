def resultado_avaliacao(imc: float): 
    """
    Resultado da avaliação 
    """   
    if imc < 18.5: 
        return "Magreza"
    elif 18.5 <= imc < 24.9: 
        return "Normal"
    elif 24.9 <= imc < 30: 
        return "Sobrepeso"
    else: 
        return "Obesidade"