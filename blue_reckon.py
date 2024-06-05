import random

def media_template(lista):
    total=0
    for elemento in lista:
        total+=elemento    
    return float("{:.2f}".format(total/len(lista)))

def simula_payload():
    # Leituras de temperatura e pH
    temperaturas = [float("{:.2f}".format(random.uniform(2, 30))) for _ in range(10)]
    ph = [float("{:.2f}".format(random.uniform(0, 14))) for _ in range(10)]

    #calculo da média
    media_temp = media_template(temperaturas)
    media_ph = media_template(temperaturas)

    #Json do protótipo
    return {"temperaturas":temperaturas,"pH":ph,"mediaTemp":media_temp,"mediapH":media_ph}

def verifica_leitura(payload):
    media_temp = payload['mediaTemp']
    media_ph = payload['mediapH']
    text = ""
    
    if media_temp < 18:
        text += f"A temperatura está abaixo do normal - {media_temp}°C\n"
    elif media_temp > 28:
        text += f"A temperatura está abaixo do normal - {media_temp}°C\n"
    else:
        text += f"A temperatura está dentro do parâmetro esperado - {media_temp}°C\n"
    
    if media_ph < 7.4:
        text += f"O pH está abaixo do normal - {media_ph} - teor ácido"   
    elif media_ph > 8.5:
        text += f"O pH está acima do normal - {media_ph} - teor alcalino"
    else:
        text += f"O pH está dentro do parâmetro esperado - {media_ph}"
        
    print("="*60)
    print(text)
    print("="*60)
    print()

def exibe_leituras(payload):
    for campo in payload:
        print("="*25)
        if campo == "temperaturas" or campo == "pH":
            print(f"Dados: {campo}")
            for leitura in range(len(payload[campo])):
                print(f"{leitura+1}° leitura: {payload[campo][leitura]}")
        else:
            print(f"{campo}: {payload[campo]}")
    print("="*25)            
                
def force_num(msg):
    resp = input(msg)
    while not resp.isnumeric():
        print("Resposta inválida")
        resp = input(msg)
    return int(resp)

def menu_selecao():
    print("Escolha uma opção!")
    print("1 - Gerar uma leitura")
    print("2 - Verificar status do sistema")
    print("3 - Exibir a última leitura do sistema")
    print("4 - Encerrar programa")
    return force_num("\nOpções -> (1|2|3|4): ")
    
    

payload = simula_payload()
run = True

while run:
    print("="*30)
    print("Bem vindo ao Blue Reckon!!!")
    print("="*30)
    opcao = menu_selecao()
    
    match opcao:
        case 1:
            payload = simula_payload()
        case 2:
            verifica_leitura(payload)
        case 3:
            exibe_leituras(payload)
        case 4:
            print("Tem certeza que deseja sair?")
            confirma = force_num("1 -> Sim | 2 -> Não: ")
            if confirma == 1:
                run = False
            elif confirma != 2:
                print("Opção inválida")
                print("Cancelando encerramento")

print("Obrigado e até logo!!!")
                
            
    
    
    
    