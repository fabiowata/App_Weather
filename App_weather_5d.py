#Importando as ferramentas para fazer as requisições.
import requests

#JSON é como uma lista ou dicionário convertido para string.
import json

import datetime

#Utilizamos o pprint como uma forma mais fácil de visualizacão. Com o programa pronto não precisamos mais dele.
##import pprint
#----------------------------------------------------------------------------------------------------------------
#Chave de acesso gerado no Accuweather
accuweatherAPIKey = 'LFlhbOIrjvJVZyfgR1EvGDc4RBAAlUoa'

#Função p/ pegar as coordenadas.
def pegarCoordenadas():
    #Pedido de requisição no site geoplugin para obter as coordenadas
    r = requests.get('http://www.geoplugin.net/json.gp')
    if (r.status_code != 200):
        print('Não foi possível obter a localização.')
        return None
    else:
        try:
            localizacao = json.loads(r.text) #converte texto json em dicionário python
            #Var de dici p/ colocar as coordenadas.
            coordenadas = {}
            #Criar uma chave 'lat' no dici p/ jogar a coordenada de latitude.
            coordenadas['lat'] = lat = localizacao['geoplugin_latitude']
            # Criar uma chave 'long' no dici p/ jogar a coordenada de longitude.
            coordenadas['long'] = long = localizacao['geoplugin_longitude']
            return coordenadas
            ##print('lat: ', lat)
            ##print('long: ', long)
        except:
            return None

#Função p/ pegar o código do local.
def pegarCodigoLocal(lat,long):

    LocationAPIUrl = 'http://dataservice.accuweather.com/locations/v1/cities/geoposition/' \
            +'search?apikey=' + accuweatherAPIKey \
                     + '&q=' + lat + '%2C%20' + long + '&language=pt-br'

    #Envio da requisição p/ o site.
    r = requests.get(LocationAPIUrl)
    #Verificação do status da requisição.
    if (r.status_code != 200):
        print('Não foi possível obter o código do local.')
        return None
    else:
        try:
            ##print(pprint.pprint(json.loads(r2.text)))
            locationResponse = json.loads(r.text)
            #Var dici p/ colocar o nome e o código do local.
            infoLocal = {}
            #Criar chave no dici p/ colocar o nome do local.
            infoLocal['nomeLocal'] = locationResponse['LocalizedName'] + ', ' \
                + locationResponse['AdministrativeArea']['LocalizedName'] + '. '\
                + locationResponse['Country']['LocalizedName']
            #Criar chave no dici p/ colocar o código do local.
            infoLocal['codigoLocal'] = locationResponse['Key']
            return infoLocal
            ##print('Código do local: ', codigoLocal)
        except:
            return None

#Função p/ pegar o dia da semana.
def pegarDiaSemana ():
    x = datetime.datetime.now().strftime('%w')

    print(x)

#Função p/ pegar a previsão do tempo.
def pegarTempoAgora(codigoLocal, nomeLocal):
    #Montagem da URL com o cod e a key inseridas automaticamente.
    # CurrentConditionsAPIUrl = "http://dataservice.accuweather.com/currentconditions/v1/"\
    #     #     + codigoLocal + "?apikey=" + accuweatherAPIKey\
    #     #     +"&language=pt-br"

    CurrentConditionsAPIUrl = "http://dataservice.accuweather.com/forecasts/v1/"\
            + "daily/5day/36369" + "?apikey=" + accuweatherAPIKey\
            + "&language=pt-br&metric=True"

    #Solicitação da requisição do tempo atual.
    r = requests.get(CurrentConditionsAPIUrl)
    #Condicional da resposta p/ imprimir p/ o cliente.
    if (r.status_code != 200):
        print('Não o clima atual.')
        return None
    else:
        try:
            #Var p/ converter a resposta de txt p/ dici python.
            CurrentConditionsResponse = json.loads(r.text)
            #Var dici p/ abrigar as informações do clima.
            infoClima = {}

            ##print(pprint.pprint(CurrentConditionsResponse))
            #Chave p/ abrigar todo texto coletado no Accweather.
            infoClima['textoClima'] = CurrentConditionsResponse[0]['WeatherText']
            #Chave p/ abrigar a temperatura.
            infoClima['temperatura'] = CurrentConditionsResponse[0]['Temperature']['Metric']['Value']
            #Chave p/ abrigar o nome do local.
            infoClima['nomeLocal'] = nomeLocal
            return infoClima
        except:
            return None


#Início do programa:
#Criar um var para facilitar as funções.



try:
    coordenadas = pegarCoordenadas()

    local = pegarCodigoLocal(coordenadas['lat'], coordenadas['long'])

    climaAtual = pegarTempoAgora(local['codigoLocal'], local['nomeLocal'])

    # Imprimir as respostas.
    print('Clima atual em: ' + climaAtual['nomeLocal'])
    print(climaAtual['textoClima'])
    print('Temperatura: ' + str(climaAtual['temperatura']) + '\xb0' + 'C')  # código \xb0 é o cogido p/ graus ceucius
except:
    print('Erro ao processar a solicitação. Entre em contato com o suporte.')


