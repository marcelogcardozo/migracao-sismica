<h1> Modelagem Sísmica </h1>

<h2> Repositório destinado ao desenvolvimento da ferramenta utilizada para modelagem sísmica </h3>

<h3> Objetivo </h4>

<p> O código tem por objetivo a geração de um <i>sismograma</i>, que por sua vez, é o registro de pontos de mesma altura ao longo do tempo. </p>

<h3> Modelo </h4>

![image](https://user-images.githubusercontent.com/54816858/117516139-9a9a5100-af6e-11eb-8248-912b1eb244b0.png)


<p> O modelo utilizado nesse código foi um modelo sintético, criado pelo Institudo Francês de Petróleo, o modelo Marmousi. Este, é baseado na geologia
  <i>offshore</i> da bacia de Cuanza, na Angola.<br><br>
    Ele possui 383 pontos no eixo X e 121 pontos no eixo Z (ou Y, Z pois se trata de profundidade). O tamanho, em pontos, do modelo pode ser ajustado
  no arquivo texto da pasta input.</p>
  
<h4> Tamanho do Modelo</h5>

<p> O tamanho real do modelo é representado por <br><br>
  
![image](https://user-images.githubusercontent.com/54816858/117515489-d3392b00-af6c-11eb-9a47-d608d09f8756.png)

  sendo Tn o tamanho do eixo n, Nn o número de pontos do eixo n e Dn a variação espacial do eixo n.<br><br>
  Com base nisso, é possível definir que
  
![image](https://user-images.githubusercontent.com/54816858/117515552-fcf25200-af6c-11eb-9b44-68c475298d01.png).

  Portanto:
  
![image](https://user-images.githubusercontent.com/54816858/117515459-bc92d400-af6c-11eb-9b67-f4e901afdaea.png)
  
  sendo <i>Vmin</i> o valor do ponto de menor valor do modelo (cada valor representa a velocidade naquele ponto), 
  <i>k</i> o número de amostras cujo padrão de melhor valor é 5 e <i>fmáx</i>, ou frequência de corte, é o valor 
  máximo da frequência da fonte.
  
  Para este trabalho foi utilizada uma frequência de corte de <i>30 Hz</i>
  
  Considerando o modelo Marmousi, a velocidade mínima é 1500, portanto <i>h = 10</i>.</p>

<h3> Termo Fonte </h3>

<br>

![image](https://user-images.githubusercontent.com/54816858/117516346-3fb52980-af6f-11eb-9ab4-80a5fa577375.png)

<p> O termo fonte é uma simulação de uma fonte (canhão de ar, dinamite, etc) da vida real.

De acordo com a propagação da onda acústica, uma parte da onda reflete em meios de diferentes densidades e outra parte refrata. 
A parte que sofrou refração é perdida, portanto, a energia da fonte só terá influência na modelagem durante um certo tempo, 
esse tempo é calculado da seguinte forma:

![image](https://user-images.githubusercontent.com/54816858/117519423-c5d66d80-af79-11eb-94d0-160a51a4b21c.png)

e como é possível observar, existe um parâmetro Dt que é a variação temporal. Seguindo o mesmo raciocínio do Dn, será possível aferir 
quanto tempo levou para que a onda gerada pela fonte percorrer o modelo.

Sendo Dt:

![image](https://user-images.githubusercontent.com/54816858/117519500-29609b00-af7a-11eb-9fc0-5090e6ddc1b1.png)

descobrimos que o tempo total é:

![image](https://user-images.githubusercontent.com/54816858/117519517-3e3d2e80-af7a-11eb-92a7-57534bcb4708.png)

sendo <i>ntotal</i> o número de passos de tempo.

E para o cálculo da função fonte, também é necessário o cálculo da frequência central da fonte. Para isso:

![image](https://user-images.githubusercontent.com/54816858/117519449-e7cff000-af79-11eb-9078-9957773bbcf5.png)

Sabendo disso, podemos calcular o <i>termo fonte</i>.

![image](https://user-images.githubusercontent.com/54816858/117519615-aab82d80-af7a-11eb-9773-0c63273f57a0.png)

<h3>Bordas Absortivas</h3>

<p> Na subsuperfície, a energia gerada pela fonte é propagada pela terra semelhante à um campo infinito. Para tentar representar o mesmo efeito no modelo sintético, é utilizada uma técnica de inclusão de bordas de absorção ao modelo, esta, terá um fator multiplicativo (<i>fat</i>) que multiplicará o valor <i>velocidade * fonte</i> para que o mesmo seja 0 ao final da borda. </p>

<h4>Bordas no Modelo</h4>

<p> O modelo com bordas será assim: </p>

![image](https://user-images.githubusercontent.com/54816858/117520302-e4d6fe80-af7d-11eb-9549-87aadaed51e6.png)

<p> E após o cálculo das bordas de acordo com o fat = 0,0025, pois é o valor com melhor resultado nos testes.
Esse cálculo é basicamente um prolongamento dos últimos pontos do modelo. </p>

![image](https://user-images.githubusercontent.com/54816858/117520240-a0e3f980-af7d-11eb-8e0d-3bc508a63e8f.png)

<h3> Equação da Onda Acústica </h3>

![image](https://user-images.githubusercontent.com/54816858/117519701-0aaed400-af7b-11eb-9f58-846984343497.png)

Sendo U, o campo de pressão no passo de tempo (n) atual.
<br><br>
Para este trabalho foi utilizado o método das diferenças finitas, que é baseado na aproximação das derivadas parciais de segunda ordem por expansão em série de Taylor de funções.<br>
Aproximação de 4ª ordem para derivadas espaciais e de 2ª ordem para derivadas temporais.


<h3> Sismograma </h3>

E como resultado da execução do código, temos o sismograma abaixo, cuja dimensão é <i>ntotal x Nn</i>. Por conta da dimensão e de que o Dt é conhecido, podemos fazer <i>ntotal x Dt</i> para descobrir o T da modelagem. 

Considerando que o valor de <i>ntotal</i> utilizado foi 9000, temos que T = 3.6s.

Portanto, temos o sismograma:

![image](https://user-images.githubusercontent.com/54816858/117520686-d558b500-af7f-11eb-8e54-90e2ffb3a9b1.png)
