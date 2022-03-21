## importar bibliotecas

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

## ferramenta de importação de arquivos
print('Analíse de Outliers')
print('Certifique-se de digitar o caminho do arquivo corretamente')
print('na versão atual a aplicação só suporta arquivos nos frmatos .csv')
arquivo_dados = input('Digite o caminho do arquivo com sua extenção:')

dataset = pd.read_csv(arquivo_dados)
## o sistema possui a limitção de não rodar com arquivos fora de padrão
## que necessitem serem setados outros parâmetros no read

dataset = dataset.fillna(0)
## subistitui os valores null por zero

numero_columuns = ((dataset.shape)[1])

log = f'Log de dados gerados na análise:\n'

def qualitativo_ou_quantitativo(dataset):
    numero_colunas = ((dataset.shape)[1])
    selecao = []
    cont = 0
    for posicao in range(numero_colunas):
        item = dataset.iloc[2,posicao]

        if (type(item) != type(True)):
            try:
                item + 1
                selecao.append(cont)
            except:
                pass
        cont = cont + 1
    return selecao

## função que define quais colunas são quantitativas, identificando as boleanas
## e separando as que podem ser usadam em operações matemáticas, assim colocando sua posição em uma lista




def coeficiente_de_variacao(dataset,indice_coluna):

    media = np.mean(dataset.iloc[:,indice_coluna])
    desvio_padrao = np.std(dataset.iloc[:,indice_coluna])
    coeficiente_variacao = desvio_padrao/media
    v0 = str(dataset.columns[indice_coluna])
    v1 = str(media)
    v2 = str(desvio_padrao)
    v3 = str(coeficiente_variacao)
    log = f'\n Para a coluna {v0}, temos: \n Média: {v1} \n Desvio Padão: {v2} \n Coeficiente de Variação: {v3} \n'

    return media, desvio_padrao, coeficiente_variacao, log

##esta função gera os parâmetros básicos de média, desvio padão
## e coeficiente de variação e gera um string com esteste dados para ser armazenado no log

def metodo_desvio(dataset, indice_coluna):
    data = dataset.iloc[:, indice_coluna]
    media = np.mean(dataset.iloc[:, indice_coluna])
    desvio_padrao = np.std(dataset.iloc[:, indice_coluna])
    parametro_corte = desvio_padrao * 3
    limite_inferior = media - parametro_corte
    limite_superior = media + parametro_corte
    outliers = data.index[(data > limite_superior) | (data < limite_inferior)].tolist()
    log = f'Detectados {len(outliers)} outliers aplicando o método do desvio padrão.\n'
    return outliers, log
## Todas as funçoes definidas abaixo com a inicial metodo, possuiem a mesma caraterística
## recebem uma base de dados, e o índice da coluna, e usam método descrito para
## identificar os outliers, retronando uma lista com o index dos outliers e uma string com a contadem dos outliers identificados.

def metodo_z_score(dataset, indice_coluna):
    data = dataset.iloc[:, indice_coluna]
    media = np.mean(dataset.iloc[:, indice_coluna])
    desvio_padrao = np.std(dataset.iloc[:, indice_coluna])
    parametro_corte = (data - media)/desvio_padrao
    outliers = data.index[(parametro_corte >= 3) | (parametro_corte <= -3)].tolist()
    log = f'Detectados {len(outliers)} outliers aplicando o método do Z-score.\n'
    return outliers, log


def metodo_desvio_absoluto_mediano(dataset, indice_coluna):
    data = dataset.iloc[:, indice_coluna]
    parametro_corte = (data - np.median(data)) / (np.median((np.abs(np.std(data)))))
    outliers = data.index[(parametro_corte >= 3) | (parametro_corte <= -3)].tolist()
    log = f'Detectados {len(outliers)} outliers aplicando o método do DAM.\n'
    return outliers, log


def metodo_Isolation_forest(dataset, indice_coluna):
    data = dataset.iloc[:, indice_coluna]
    i_forest = IsolationForest(n_estimators=250, contamination=0.03)
    dados = data.values.reshape(-1,1)
    i_forest.fit(dados)
    dataset['anomalia'] = i_forest.predict(dados)
    anomalias = dataset.loc[dataset['anomalia'] == -1]
    outliers = list(anomalias.index)
    log = f'Detectados {len(outliers)} outliers aplicando o método Isolation Forest.\n'
    return outliers, log

def metodo_boxplot(dataset, indice_coluna):
    data = dataset.iloc[:, indice_coluna]
    Q3 = data.quantile(0.75)
    Q1 = data.quantile(0.25)
    Interquartil = Q3 - Q1
    limite_inferior = Q1 - (Interquartil * 1.5)
    limite_superior = Q3 + (Interquartil * 1.5)
    outliers = data.index[(data > limite_superior) | (data < limite_inferior)].tolist()
    log = f'Detectados {len(outliers)} outliers aplicando o método Boxplot.\n'
    return outliers, log


def grava_log(log):
    text_file = open("log.txt", "w")
    save = text_file.write(log)
    text_file.close()
## esta função pega o log final e gera o arquivo log.txt com os resultados da análise

def gera_analise(dataset,log):
    selecao = (qualitativo_ou_quantitativo(dataset))
    for indice in selecao:
        log = log + (coeficiente_de_variacao(dataset, indice)[3])
        log = log + (metodo_desvio(dataset, indice)[1])
        log = log + (metodo_z_score(dataset, indice)[1])
        log = log + (metodo_desvio_absoluto_mediano(dataset, indice)[1])
        log = log + (metodo_Isolation_forest(dataset, indice)[1])
        log = log + (metodo_boxplot(dataset, indice)[1])
        log = log + '\n'
    grava_log(log)
    return log

##esta função excuta os métodos em todas as colunas identificadas como quantitativas,
## depoi concatena os logs gerados de cada análise e ao final retorna uma string contendo o log geral.
## esta função também chama a função de gravação para gerar com base no log final o arquivo log.txt

def exclui_outliers(dataset,indice_coluna):
    print(f'selecione o tipo de método para exclusão:\n'
          f'Dos Outliers da Coluna: {dataset.columns[indice_coluna]}\n'
          '1 - Para Método do Desvio Padrão\n'
          '2 - Para Método Z-Score\n'
          '3 - Para Metodo Desvio Absoluto Mediano\n'
          '4 - Para Método Isolation Forest\n'
          '5 - Para Método Boxplot\n'
          '0 - Para Sair')
    tipo = input('Digite o Número do Método Desejado:')
    tipo = int(tipo)
    print(tipo ==1)
    selecao = []
    opcoes_possiveis = [1,2,3,4,5]
    if tipo == 1:
        selecao = metodo_desvio(dataset, indice_coluna)[0]
    if tipo == 2:
        selecao = metodo_z_score(dataset, indice_coluna)[0]
    if tipo == 3:
        selecao = metodo_desvio_absoluto_mediano(dataset, indice_coluna)[0]
    if tipo == 4:
        selecao = metodo_Isolation_forest(dataset, indice_coluna)[0]
    if tipo == 5:
        selecao = metodo_boxplot(dataset, indice_coluna)[0]
    if not(tipo in opcoes_possiveis):
        print(f'Pulado o tratamento para a coluna:  {dataset.columns[indice_coluna]}')
    dataset = dataset.drop(selecao)
    return dataset
##esta função auxiliar recebe o dataset, o índice da coluna e pergunta qual método deve ser ussado para identificar os outliers,
## depois gera uma lista com os outliers e usa esta lista gerada para excluir as linhas com outliers.

def processa_exclusao (dataset):
    seleciona = (qualitativo_ou_quantitativo(dataset))
    for indice in seleciona:
        dataset = exclui_outliers(dataset, indice)
        print(dataset.shape)
## esta função chama a função assima para todas as colunas com dados qualitativos, tornando possível escolher quais linhas aplicar a exclusão
## bem como o método empregado.


def exclui_outliers_mesmo_metodo(dataset):
    print(f'selecione o tipo de método para exclusão Dos Outliers:\n'
          '1 - Para Método do Desvio Padrão\n'
          '2 - Para Método Z-Score\n'
          '3 - Para Metodo Desvio Absoluto Mediano\n'
          '4 - Para Método Isolation Forest\n'
          '5 - Para Método Boxplot\n'
          '0 - Para Sair')
    tipo = input('Digite o Número do Método Desejado:')
    tipo = int(tipo)
    print(tipo ==1)
    selecao = []
    opcoes_possiveis = [1,2,3,4,5]
    seleciona = (qualitativo_ou_quantitativo(dataset))
    for indice in seleciona:
        print(dataset.shape)
        if tipo == 1:
            selecao = metodo_desvio(dataset, indice)[0]
        if tipo == 2:
            selecao = metodo_z_score(dataset, indice)[0]
        if tipo == 3:
            selecao = metodo_desvio_absoluto_mediano(dataset, indice)[0]
        if tipo == 4:
            selecao = metodo_Isolation_forest(dataset, indice)[0]
        if tipo == 5:
            selecao = metodo_boxplot(dataset, indice)[0]
        if not(tipo in opcoes_possiveis):
            print(f'Pulada a exlusão')
        dataset = dataset.drop(selecao)
    return dataset

## esta função é similar a de exlusão porém aplica o mesmo método para todas as colunas.

print('Selecione o método de exclusão:\n'
      '1 - para selecionar um método diferente para cada colunas ou pular colunas \n'
      '2 - para aplicar o mesmo método em todas as colunas\n'
      '3 - para gerar um log.txt com uma análise de outliers'
      '4 - para Sair\n')
opcao_selecionada = int(input('Digite a opção desejada:'))

possibilidades_de_escolha = [1,2,3]
if opcao_selecionada == 1:
    dataset = processa_exclusao(dataset)
    dataset.to_csv('arquivo_tarado.csv')
if opcao_selecionada == 2:
    dataset = exclui_outliers_mesmo_metodo(dataset)
    dataset.to_csv('arquivo_tarado.csv')
if opcao_selecionada == 2:
    gera_analise(dataset,log)
if not(opcao_selecionada in possibilidades_de_escolha):
    print('Você selecionou Sair ou uma opção inválida\n'
          'A aplicação será encerrada!!!')

## parte final da aplicação devolve um arquivo tratado baseado na sua escolha ou gera um log de análise.