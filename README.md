# Projeto de Migração Sísmica

Este projeto implementa um algoritmo de **Migração Sísmica** em Python, acelerado com o uso da biblioteca **NumPy** para operações vetorizadas e cálculo eficiente de grandes matrizes de dados. O foco do projeto é processar dados sísmicos brutos para a criação de imagens que representem as estruturas geológicas do subsolo.

## Índice

- [Projeto de Migração Sísmica](#projeto-de-migração-sísmica)
  - [Índice](#índice)
  - [Introdução](#introdução)
    - [Objetivos principais do projeto](#objetivos-principais-do-projeto)
  - [Site do Projeto](#site-do-projeto)
  - [Instalação](#instalação)
  - [Como usar](#como-usar)
  - [Próximos Passos](#próximos-passos)
  - [Contribuições](#contribuições)

## Introdução

A **migração sísmica** é uma técnica utilizada para aprimorar a interpretação de dados sísmicos, ajustando a posição dos reflexos para compensar a profundidade e complexidade das camadas geológicas. Este projeto foi desenvolvido utilizando **Python** e **NumPy** para lidar com os cálculos pesados e foi otimizado para desempenho com a paralelização interna que o NumPy oferece.

Este repositório está em constante desenvolvimento e possui como foco principal a migração de dados em 2D, com potencial expansão para 3D no futuro.

### Objetivos principais do projeto

- **Implementação básica de migração sísmica**
- **Aceleração dos cálculos com NumPy**
- **Possibilitar processamento de grandes volumes de dados sísmicos**

## Site do Projeto

Acesse o site oficial do projeto para mais detalhes sobre a aplicação:

[https://marcelogcardozo.github.io/migracao-sismica/](https://marcelogcardozo.github.io/migracao-sismica/)

## Instalação

Para rodar o projeto, siga os passos abaixo:

1. Clone este repositório:

   ```bash
   git clone https://github.com/marcelogcardozo/migracao-sismica.git
   cd migracao-sismica
   ```

2. Crie o ambiente virtual e instale as dependências com poetry:

   ```bash
   poetry install
   ```

## Como usar

1. Altere o arquivo `app.config.json` com os parâmetros desejados
2. Adicione o seu modelo binário da seção na pasta `bin`
3. Execute a aplicação:
   ```bash
   poetry run python -m app.main
   ```

## Próximos Passos

- Suavização do Modelo: Implementar técnicas de suavização para lidar com transições abruptas de velocidade no modelo geológico.
- Otimização com Numba: Utilizar o Numba para compilar partes críticas do código Python para código nativo e acelerar ainda mais os cálculos.
- Verificação de Cálculo no Tempo Presente: Revisar e otimizar o cálculo da matriz no tempo presente, assegurando a correta alocação temporal dos eventos sísmicos.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests com melhorias ou correções.

Para contribuir, siga os passos:

1. Faça um fork do projeto.
2. Crie uma branch para sua feature:
   ```bash
   git checkout -b minha-feature
   ```
3. Commit suas alterações:
   ```bash
   git commit -m 'Adiciona minha nova feature'
   ```
4. Envie um push para a branch:
   ```bash
   git push origin minha-feature
   ```
5. Abra um pull request.
