###############################################################################
# Univesidade Federal de Pernambuco -- UFPE (http://www.ufpe.br)
# Centro de Informatica -- CIn (http://www.cin.ufpe.br)
# Bacharelado em Sistemas de Informacao
# IF968 -- Programacao 1
#
# Autor:    Marcos Vinicius Holanda Borges
#           Maria Eugênia Pereira dos Santos
#
# Email:    mvhb@cin.ufpe.br
#           meps@cin.ufpe.br
#
# Data:        2016-06-10
#
# Descricao:  Este e' um modelo de arquivo para ser utilizado para a implementacao
#                do projeto pratico da disciplina de Programacao 1. 
#                 A descricao do projeto encontra-se no site da disciplina e trata-se
#                de uma adaptacao do projeto disponivel em 
#                http://nifty.stanford.edu/2016/manley-urness-movie-review-sentiment/
#                O objetivo deste projeto e' implementar um sistema de analise de
#                sentimentos de comentarios de filmes postados no site Rotten Tomatoes.
#
# Licenca: The MIT License (MIT)
#          Copyright(c) 2016 Marcos Vinicius Holanda Borges, Maria Eugênia Pereira dos Santos
#
###############################################################################
import sys
import re
#arquivoBase = open("trainSet.txt", "r")
#entrada = open("testSet.txt","r")

def clean_up(s):
    punctuation = ''''!"',;:.-?)([]<>*#\n\t\r'''
    result = s.lower().strip(punctuation)
    return result

def split_on_separators(original, separators):

    '''    Retorna um vetor de strings nao vazias obtido a partir da quebra
        da string original em qualquer dos caracteres contidos em 'separators'.
        'separtors' e' uma string formada com caracteres unicos a serem usados
        como separadores. Por exemplo, '^$' e' uma string valida, indicando que
        a string original sera quebrada em '^' e '$'.
    '''
    lista=[]
    fraseCerta = ""
    x=list(filter(lambda x: x != '',re.split('[{0}]'.format(separators),original)))
    for k in x:
        k = clean_up(k) #aplicando a clean_up na frase
        if k !=" " and k !="''":
            lista.append(k) #adicionando numa nova lista a frase corrigida
    for j in lista:
        fraseCerta = fraseCerta + " " + j
    return fraseCerta[1:len(fraseCerta)-1] #retornando a frase correta presente

def readTrainingSet(arquivoBase):
    '''    Recebe o caminho do arquivo com o conjunto de treinamento como parametro
        e retorna um dicionario com triplas (palavra,freq,escore) com o escore
        medio das palavras no comentarios.
    '''
    arquivoBase = open(arquivoBase, "r")
    stop = open("stopwords.txt","r")
    wordsFreq = {}
    wordPoint = {}
    wordScore = {}
    words = {}
    listaStopWords = []
    listaFrasesNotas = []
    todasPalavrasBase = []
    palavrasBoas = []
    
    for line in arquivoBase:
        line=split_on_separators(line," ") #limpando as reviews
        listaReviews = line.split(" ")[2:] #tirando a nota e o espaco da review
        reviewScore = line[0] #pegando apenas as notas
        todasPalavrasBase+= listaReviews #pegando palavra por palavra das reviews
        listaFrasesNotas.append((listaReviews,reviewScore)) #salvando numa lista final as tuplas 

    for x in stop:
        x=x.replace("\n","")
        listaStopWords.append(x) #criando a lista de stop words
    for g in todasPalavrasBase:
        if g not in listaStopWords: #se essa palavra for de stop words, retira ela
            if g !='':
                palavrasBoas.append(g) #coloca numa lista de palavras que expressam sentimento

    listaSemRepeticao = set(palavrasBoas) #tirar repeticao de palavras
    for palavra in listaSemRepeticao:
        contador = 0
        score = 0
        for word,nota in listaFrasesNotas:
            for palavras in word: #passando pelas tuplas comparando as palavras da tupla com as palavras da lista de palavras sem repeticoes
                    if palavra == palavras: #sendo igual, aumenta a frequencia
                            contador += 1
                            score += int(nota) #somando tambem as notas de todas as vezes q a palavra aparece

        wordsFreq[palavra] = contador
        wordPoint[palavra] = score
        wordScore[palavra] = wordPoint[palavra]/wordsFreq[palavra]
        wordScore[palavra]= round(wordScore[palavra],2) #arredondamento 
        words[(palavra)] = (wordsFreq[palavra],wordScore[palavra])
        
    arquivoBase.close()
    stop.close()
    return words    

def readTestSet(entrada):
    """Esta funcao le o arquivo contendo o conjunto de teste
	retorna um vetor/lista de pares (escore,texto) dos
	comentarios presentes no arquivo."""
    entrada = open(entrada,"r")
    #listaTeste=[]
    listaDePares=[]
    for k in entrada:
        frase= k[1:] #pegando apenas a frase sem a nota
        frase = clean_up(frase)
        listaDePares.append((int(k[0]),frase[1:])) #adicionando numa lista as reviews com suas notas em forma de tuplas
        reviews=listaDePares
    entrada.close()
    return reviews

def computeSentiment(review,words):
    ''' Retorna o sentimento do comentario recebido como parametro.
        O sentimento de um comentario e' a media dos escores de suas
        palavras. Se uma palavra nao estiver no conjunto de palavras do
        conjunto de treinamento, entao seu escore e' 2.
        Review e' a parte textual de um comentario.
        Words e' o dicionario com as palavras e seus escores medios no conjunto
        de treinamento.
    '''
    stop = open("stopwords.txt","r")
    removerStops = []
    for m in stop:
        m=m.replace("\n","")
        removerStops.append(m) #lista com as stop words
        
    listaNotas=[]
    string=review.split()
    for x in string:
        if x not in removerStops:
            if x in words.keys():
                listaNotas.append(words[x][1])
            else:
                listaNotas.append(2)
    stop.close()
    if len(listaNotas) >0:
        return round((sum(listaNotas))/len(listaNotas),2)
    else:
        return "Frase apenas com stop words"

def computeSumSquaredErrors(reviews,words):
    '''    Computa a soma dos quadrados dos erros dos comentarios recebidos
        como parametro. O sentimento de um comentario e' obtido com a
        funcao computeSentiment. 
        Reviews e' um vetor de pares (escore,texto)
        Words e' um dicionario com as palavras e seus escores medios no conjunto
        de treinamento.    
    '''
    quantidade = 0
    sse = 0   
    for x in reviews:
        notaProg = computeSentiment(x[1],words) #nota da frase pela base no trainset
        if notaProg != "Frase apenas com stop words":
            diferenca = notaProg - x[0] 
            if diferenca <0:
                diferenca = diferenca * - 1
            sse = sse + (diferenca**2)
            quantidade +=1
            notaProg = 0
        else:
            quantidade +=1
            notaProg = 0
    return sse/quantidade 

def main():
    
    # Os arquivos sao passados como argumentos da linha de comando para o programa
    # Voce deve buscar mais informacoes sobre o funcionamento disso (e' parte do
    # projeto).
    
    # A ordem dos parametros e' a seguinte: o primeiro e' o nome do arquivo
    # com o conjunto de treinamento, em seguida o arquivo do conjunto de teste.
    
    if len(sys.argv) < 3:
        print ('Numero invalido de argumentos')
        print ('O programa deve ser executado como python sentiment_analysis.py <arq-treino> <arq-teste>')
        sys.exit(0)

    # Lendo conjunto de treinamento e computando escore das palavras
    words = readTrainingSet(sys.argv[1])
    
    # Lendo conjunto de teste
    reviews = readTestSet(sys.argv[2])
    
    # Inferindo sentimento e computando soma dos quadrados dos erros
    sse = computeSumSquaredErrors(reviews,words)
    
    print ('A soma do quadrado dos erros e\': {0}'.format(sse))
            

if __name__ == '__main__':
   main()    

