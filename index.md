<h1> Modelagem Sísmica </h1>

<h2> Objetivo </h2>

<p> &nbsp;&nbsp;&nbsp;&nbsp;O código tem por objetivo a geração de um <i>sismograma</i>, que por sua vez, é o registro de pontos de mesma altura ao longo do tempo. </p>
<br>
<h2> Modelo </h2>

<img src="https://user-images.githubusercontent.com/54816858/117524851-df85ae00-af95-11eb-8c48-1a6871cd3abe.png" alt="drawing" width="600"/>

<p> &nbsp;&nbsp;&nbsp;&nbsp;O modelo utilizado nesse código foi um modelo sintético, criado pelo Institudo Francês de Petróleo, o modelo Marmousi. Este, é baseado na geologia
  <i>offshore</i> da bacia de Cuanza, na Angola.<br><br>
    &nbsp;&nbsp;&nbsp;&nbsp;Ele possui 383 pontos no eixo X e 121 pontos no eixo Z (ou Y, Z pois se trata de profundidade). O tamanho, em pontos, do modelo pode ser ajustado
  no arquivo texto da pasta input.</p>
  
<h3> Tamanho do Modelo</h3>

<p> O tamanho real do modelo é representado por </p>
  
  
<a href="https://www.codecogs.com/eqnedit.php?latex=Tn&space;=&space;Nn&space;\cdot&space;Dn" target="_blank"><img src="https://latex.codecogs.com/png.latex?Tn&space;=&space;Nn&space;\cdot&space;Dn" title="Tn = Nn \cdot Dn" /></a>


<p>sendo Tn o tamanho do eixo n, Nn o número de pontos do eixo n e Dn a variação espacial do eixo n.<br><br>
Com base nisso, é possível definir que</p>
  
  
<a href="https://www.codecogs.com/eqnedit.php?latex=Dn&space;=&space;Dy&space;=&space;Dx&space;=&space;h" target="_blank"><img src="https://latex.codecogs.com/png.latex?Dn&space;=&space;Dy&space;=&space;Dx&space;=&space;h" title="Dn = Dy = Dx = h" /></a>.


<p>Portanto:</p>
  
<a href="https://www.codecogs.com/eqnedit.php?latex=h&space;\leq&space;\frac{Vmin}{k&space;\cdot&space;fmax}" target="_blank"><img src="https://latex.codecogs.com/png.latex?h&space;\leq&space;\frac{Vmin}{k&space;\cdot&space;fmax}" title="h \leq \frac{Vmin}{k \cdot fmax}" /></a>
  
<p>sendo <i>Vmin</i> o valor do ponto de menor valor do modelo (cada valor representa a velocidade naquele ponto), 
<i>k</i> o número de amostras cujo padrão de melhor valor é 5 e <i>fmáx</i>, ou frequência de corte, é o valor 
  máximo da frequência da fonte.
  
  Para este trabalho foi utilizada uma frequência de corte de <i>30 Hz</i>
  
  Considerando o modelo Marmousi, a velocidade mínima é 1500, portanto <i>h = 10</i>.</p>

<br>
<h2> Termo Fonte </h2>

<img src="https://user-images.githubusercontent.com/54816858/117525374-5e7be600-af98-11eb-9c29-b2c1913d2160.png" alt="drawing" width="500"/>


<p> O termo fonte é uma simulação de uma fonte (canhão de ar, dinamite, etc) da vida real.

De acordo com a propagação da onda acústica, uma parte da onda reflete em meios de diferentes densidades e outra parte refrata. 
A parte que sofrou refração é perdida, portanto, a energia da fonte só terá influência na modelagem durante um certo tempo, 
esse tempo é calculado da seguinte forma:</p>


<a href="https://www.codecogs.com/eqnedit.php?latex=Nf&space;=&space;\frac{4&space;\cdot&space;\sqrt{\pi}}{fcorte&space;\cdot&space;Dt}" target="_blank"><img src="https://latex.codecogs.com/png.latex?Nf&space;=&space;\frac{4&space;\cdot&space;\sqrt{\pi}}{fcorte&space;\cdot&space;Dt}" title="Nf = \frac{4 \cdot \sqrt{\pi}}{fcorte \cdot Dt}" /></a>


<p>e como é possível observar, existe um parâmetro Dt que é a variação temporal. Seguindo o mesmo raciocínio do Dn, será possível aferir 
quanto tempo levou para que a onda gerada pela fonte percorrer o modelo.<br>

Sendo Dt:</p>


<a href="https://www.codecogs.com/eqnedit.php?latex=Dt&space;=&space;\frac{h}{\mu&space;\cdot&space;\sqrt{Vmax}}" target="_blank"><img src="https://latex.codecogs.com/png.latex?Dt&space;=&space;\frac{h}{\mu&space;\cdot&space;\sqrt{Vmax}}" title="Dt = \frac{h}{\mu \cdot \sqrt{Vmax}}" /></a>


<p>descobrimos que o tempo total é:</p>


<a href="https://www.codecogs.com/eqnedit.php?latex=T&space;=&space;ntotal&space;\cdot&space;Dt" target="_blank"><img src="https://latex.codecogs.com/png.latex?T&space;=&space;ntotal&space;\cdot&space;Dt" title="T = ntotal \cdot Dt" /></a>


<p>sendo <i>ntotal</i> o número de passos de tempo.

E para o cálculo da função fonte, também é necessário o cálculo da frequência central da fonte. Para isso:</p>


<a href="https://www.codecogs.com/eqnedit.php?latex=Fc&space;=&space;\frac{fcorte}{3&space;\cdot&space;\sqrt{\pi}}" target="_blank"><img src="https://latex.codecogs.com/png.latex?Fc&space;=&space;\frac{fcorte}{3&space;\cdot&space;\sqrt{\pi}}" title="Fc = \frac{fcorte}{3 \cdot \sqrt{\pi}}" /></a>


<p>Sabendo disso, podemos calcular o <i>termo fonte</i>.</p>


<a href="https://www.codecogs.com/eqnedit.php?latex=f(t)&space;=&space;[1&space;-&space;2\pi&space;(\pi&space;\cdot&space;Fc&space;\cdot&space;t)^{2}]&space;\cdot&space;e^{-\pi&space;(\pi&space;\cdot&space;Fc&space;\cdot&space;t)^{2}}" target="_blank"><img src="https://latex.codecogs.com/png.latex?f(t)&space;=&space;[1&space;-&space;2\pi&space;(\pi&space;\cdot&space;Fc&space;\cdot&space;t)^{2}]&space;\cdot&space;e^{-\pi&space;(\pi&space;\cdot&space;Fc&space;\cdot&space;t)^{2}}" title="f(t) = [1 - 2\pi (\pi \cdot Fc \cdot t)^{2}] \cdot e^{-\pi (\pi \cdot Fc \cdot t)^{2}}" /></a>

<br>
<h2>Bordas Absortivas</h2>

<p> &nbsp;&nbsp;&nbsp;&nbsp;Na subsuperfície, a energia gerada pela fonte é propagada pela terra semelhante à um campo infinito. Para tentar representar o mesmo efeito no modelo sintético, é utilizada uma técnica de inclusão de bordas de absorção ao modelo, esta, terá um fator multiplicativo (<i>fat</i>) que multiplicará o valor <i>velocidade * fonte</i> para que o mesmo seja 0 ao final da borda. </p>

<h3>Bordas no Modelo</h3>

<p> O modelo com bordas será assim: </p>

<img src="https://user-images.githubusercontent.com/54816858/117525074-19a37f80-af97-11eb-8fdc-a226b871a28e.png" alt="drawing" width="600"/>

<p> E após o cálculo das bordas de acordo com </p>

<a href="https://www.codecogs.com/eqnedit.php?latex=fat&space;=&space;0.0025" target="_blank"><img src="https://latex.codecogs.com/png.latex?fat&space;=&space;0.0025" title="fat = 0.0025" /></a>,

<p>pois é o valor com melhor resultado nos testes.
Esse cálculo é basicamente um prolongamento dos últimos pontos do modelo. </p>

<img src="https://user-images.githubusercontent.com/54816858/117525093-32139a00-af97-11eb-87e4-29dee3aae826.png" alt="drawing" width="600"/>

<br>
<h2> Equação da Onda Acústica </h2>


<a href="https://www.codecogs.com/eqnedit.php?latex=\frac{\partial&space;P}{\partial&space;x^{2}}&space;&plus;&space;\frac{\partial&space;P}{\partial&space;y^{2}}&space;&plus;&space;\frac{\partial&space;P}{\partial&space;z^{2}}&space;=&space;f(t)" target="_blank"><img src="https://latex.codecogs.com/png.latex?\frac{\partial&space;P}{\partial&space;x^{2}}&space;&plus;&space;\frac{\partial&space;P}{\partial&space;y^{2}}&space;&plus;&space;\frac{\partial&space;P}{\partial&space;z^{2}}&space;=&space;f(t)" title="\frac{\partial P}{\partial x^{2}} + \frac{\partial P}{\partial y^{2}} + \frac{\partial P}{\partial z^{2}} = f(t)" /></a>


<p>Sendo P, o campo de pressão no passo de tempo (n) atual.
<br><br>
Para este trabalho foi utilizado o método das diferenças finitas, que é baseado na aproximação das derivadas parciais de segunda ordem por expansão em série de Taylor de funções.<br>
Aproximação de 4ª ordem para derivadas espaciais e de 2ª ordem para derivadas temporais.</p>

<br>
<h2> Sismograma </h2>

<p>Por conta da dimensão e Dt que é conhecido, podemos descobrir o T da modelagem. </p>

<p>Dessa forma, no eixo Y temos que:</p>
<a href="https://www.codecogs.com/eqnedit.php?latex=ntotal&space;=&space;9000" target="_blank"><img src="https://latex.codecogs.com/png.latex?ntotal&space;=&space;9000" title="ntotal = 9000" /></a><br>
<a href="https://www.codecogs.com/eqnedit.php?latex=Dt&space;=&space;0.0004" target="_blank"><img src="https://latex.codecogs.com/png.latex?Dt&space;=&space;0.0004" title="Dt \cong 0.0004" /></a><br>
<a href="https://www.codecogs.com/eqnedit.php?latex=T&space;\cong&space;3.6&space;s" target="_blank"><img src="https://latex.codecogs.com/png.latex?T&space;\cong&space;3.6&space;s" title="T \cong 3.6 s" /></a>
<br><br>
<p> Já no eixo X: </p>
<a href="https://www.codecogs.com/eqnedit.php?latex=Nx&space;=&space;383" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Nx&space;=&space;383" title="Nx = 383" /></a><br>
<a href="https://www.codecogs.com/eqnedit.php?latex=h&space;=&space;10" target="_blank"><img src="https://latex.codecogs.com/gif.latex?h&space;=&space;10" title="h = 10" /></a><br>
<a href="https://www.codecogs.com/eqnedit.php?latex=Tx&space;=&space;3830&space;m" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Tx&space;=&space;3830&space;m" title="Tx = 3830 m" /></a>
<br>
<br>

<p>E como resultado da execução do código, temos o sismograma abaixo, cuja dimensão é </p>

<a href="https://www.codecogs.com/eqnedit.php?latex=Dim&space;=&space;3.6&space;s&space;\times&space;3.8&space;Km" target="_blank"><img src="https://latex.codecogs.com/gif.latex?Dim&space;=&space;3.6&space;s&space;\times&space;3.8&space;Km" title="Dim = 3.6 s \times 3.8 Km" /></a>
<br>

<img src="https://user-images.githubusercontent.com/54816858/117525318-00e79980-af98-11eb-8c51-6ba407c7790e.png" alt="drawing" width="600"/>
