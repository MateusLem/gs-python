import serial
import json
import random

def force_num(msg:str) -> int:
    '''Força que o input do usuário seja um numeral'''
    resp = input(msg)
    while not resp.isnumeric():
        print("Resposta inválida")
        resp = input(msg)
    return int(resp)

def force_yes_no(msg:str) -> int:
    '''Força que o input do usuário seja 1 -> Sim ou 2 -> Não'''
    print(msg)
    resp = input("1 -> Sim | 2 -> Não: ")
    while not resp.isnumeric() and resp != '1' and resp != '2':
        print("Resposta inválida")
        resp = input("1 -> Sim | 2 -> Não: ")
    return int(resp)

def media_template(lista:list) -> float:
    '''
    Permite calcular médias de listas de forma genérica.
    Retorna o resultado como float com 2 casas decimais
    '''
    total=0
    for elemento in lista:
        total+=elemento    
    return float("{:.2f}".format(total/len(lista)))

def verifica_leitura(payload:dict) -> None:
    '''Verifica os campos de "média" da leitura e exibe uma mensagem condizente com os dados lidos'''
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
    
    # Exibição do texto com formatação para melhor leitura do usuário
    print("="*60)
    print(text)
    print("="*60+"\n")

def exibe_leituras(payload:dict) -> None:
    '''Lê o payload enviado pelo Arduino e formata-o para ser lido, pensando na melhor experiência do usuário'''
    for campo in payload:
        print("="*25)
        # Separa as exibições de média das demais, uma vez que são apenas um valor, e não uma lista de dados
        if 'media' in campo:
            print(f"{campo}: {payload[campo]}") 
        else:
            print(f"Dados: {campo}")
            for leitura in range(len(payload[campo])):
                print(f"{leitura+1}° leitura: {payload[campo][leitura]}")
                
    print("="*25+"\n")            
  
def read_serial() -> dict:
    '''Lê o monitor Serial do Arduino, e converte o json impresso como dicionário'''
    ser = serial.Serial(serial_port, baud_rate)
    while True:
        if ser.in_waiting > 0:
            json_data = ser.readline().decode('utf-8').strip()
            if json_data:
                ser.close()
                return json.loads(json_data)
              
def simula_payload() -> dict:
    '''Simula uma leitura de payload do Arduino enviada pelo monitor Serial'''
    # Leituras de temperatura e pH
    temperaturas = [float("{:.2f}".format(random.uniform(2, 30))) for _ in range(10)]
    ph = [float("{:.2f}".format(random.uniform(0, 14))) for _ in range(10)]

    #Calculo das médias
    media_temp = media_template(temperaturas)
    media_ph = media_template(temperaturas)

    #Json do protótipo
    return {"temperaturas":temperaturas,"pH":ph,"mediaTemp":media_temp,"mediapH":media_ph}

def verifica_arduino() -> dict:
    '''Verifica se o Arduino está conectado'''
    if arduino:
        return read_serial()
    return simula_payload()

# Configurações do Arduino
# ALTERAR CONFORME SUA NECESSIDADE
serial_port = 'COM1'
baud_rate = 9600

# Configuração de execução
arduino = True # Pressupõe que o usuário está com o Arduino conectado
run = True # Força execução do programa

conn = force_yes_no("O Arduino está conectado?")
if conn == 2:
    arduino = False
    conn = force_yes_no("Você deseja conecta-lo?\nLembrando que uma vez iniciado, não será possível conecta-lo mais.") # Em caso negativo, pressupõe-se que o usuário quer apenas simular o funcionamento do Arduino
    if conn == 1: 
        print("Beleza!!!")
        print("Como o Arduino precisa estar previamente conectado para funcionar, vamos encerrar o programa por aqui!")
        run = False
    
if run:
    payload = verifica_arduino()
    while run:
        print("="*30)
        print("Bem vindo ao Blue Reckon!!!")
        print("="*30)
        
        print("Escolha uma opção!")
        print("1 - Gerar uma leitura")
        print("2 - Verificar status do sistema")
        print("3 - Exibir a última leitura do sistema")
        print("4 - Encerrar programa")
        opcao = force_num("\nOpções -> (1|2|3|4): ")
        
        match opcao:
            case 1:
                payload = verifica_arduino()
            case 2:
                verifica_leitura(payload)
            case 3:
                exibe_leituras(payload)
            case 4:
                # Confirmação do encerramento
                confirma = force_yes_no('Tem certeza que quer sair?')
                if confirma == 1:
                    print("Encerrando programa")
                    run = False
                else:
                    print("Cancelando encerramento")

print("Obrigado e até logo!!!")