20010116
Revista da FAPESP - tabelas

20010112
BVSLaw - o campo 67 de country nao estava sendo carregado com a nova versao, provocando erro na recupera��o das palavras.
	- alterei tamb�m a montagem da estrutura das leis. Era gerado o mesmo valor de chave para conte�dos em escopos diferentes.


20010110
Lilacs - campo 38=nd -> nao enviar o campo 38
BVSLaw - inclus�o de atributos para leis internacionais
	- faltou inserir o campo 67 de pa�s no registro lilacs
	- novo campo em lawmod12 -> campo 904 para conte�dos repetitivos
	- como inserir dados de link??? -> 
		- texto do link est� no campo 203^l (repetitivo)
		- as informa��es do link est�o no campo 37 (repetitivo)
		- testes com link.pft (guardado em library\bvslaw)


20010109
BVSLaw - link -> bvslaw 1.2, inclusao de atributos para link


20010204
SciELO - scielo.ini -> apresenta��o dos t�tulos das revistas no formul�rio, excluindo as revistas usadas somente para relat�rios e altera��o do programa para n�o incluir linhas em branco no combo do formul�rio para as revistas exclu�das

20010203
BVSLaw - estrutura de diret�rios
	escopo apenas para leitura e comparacao com o documento -> modifica��o no arquivo bvslaw.ini em [CfgRec] e 
[DirInfo]

LILACS - cria��o de uma fun��o que completa a localiza��o da afilia��o


20010201
BVSLaw - library
incluir atributos novos: lorgname, esource, scopegrp
alteracoes dos atributos: 
	authorsp - aparece em mais um nivel
	country - repetitivo
	title	- repetitivo, a marcacao deve inserir o caracter % entre cada ocorrencia. Alteracao no conversor para aceitar %.
		


20001222
Bvslaw - library
Erro na descricao das tabelas para os elementos flutuantes quando eles aparecem no front e no back.


20001219
- tratamento de part sem header
- article, paragraph, etc muito grandes, nao cabem em um �nico registro, dividir em mais de um.
- lilacs: 
	campo 38: codigo em minuscula, nd = "", fig = ilus
	campo 8: url do artigo


20001218
- tratamento de part sem header
- article, paragraph, etc muito grandes, nao cabem em um �nico registro, dividir em mais de um.

20001215
BVSLaw 
- tratamento de part sem header
- article, paragraph, etc muito grandes, nao cabem em um �nico registro, dividir em mais de um.

20001214
Deixar  o menu habilitado opcionalmente para Administracao das bd.

20001212
Thesis
Arquivos de entrada e library e labels
Inclui campo 709 para guardar o nome da DTD
Os nomes dos diretorios em caixa baixa.

20001127
Fazer os descritores tag scheme, campo 85, repetitiva, acompanhando cada keyword.
Alterei artmodel os registros de scheme e keyword, acrescentando em ambos o campo v5 com conteudo keygrp:, assim sendo, o conteudo de cada campo v85 (scheme ou keyword) sao ligados por um indice, isto �, o conte�do do subcampo ^i.

20001121
Administra��o das Bases de Dados - Recriar a base iso-list

20001116 - bvslaw
Testes - Arquivo com estouro do limite de registro

20001116 - bvslaw
Arquivo com estouro do limite de registro.

20001116
Para procurar as refer�ncias do markup no texto completo, estava faltando remover do body as entidades &lt; e &gt;, as quais foram incluidas no arquivo enthtml.txt do diretorio common.

Titulo das revistas no registro l da Lilacs nao estava sendo convertido para DOS.

20001113
Adminsitracao da base de dados - Regerar a base de administracao a partir das bases de dados que foram geradas pelo conversor

20001108
Procurar simplificar o conversor
Funcao para administrar a base de dados para gerar registros na base de administracao para as bases geradas antes da existencia desta base de administracao.

20001107
Para procurar as refer�ncias do markup no texto completo, estava faltando remover do markup as entidades, al�m disso, na funcao de busca por uma referencia estava incorreto o modo de atualizar as informacoes da 'compactacao' das refer�ncias marcadas e, por isso, a funcao nao conseguia encontrar as demais.

20001031
Adminsitracao da base de dados
Permitir que sejam apagadas as bases criadas pelo conversor

20001019
Form About

Versao generica do conversor
Lilacs