# 📈 Análise de Sentimentos de Tweets sobre Companhias Aéreas ✈️

Em um cenário onde as opiniões dos consumidores sobre companhias aéreas estão cada vez mais presentes nas redes sociais, identificar e entender os sentimentos dos usuários é fundamental para as empresas se adaptarem e melhorarem seus serviços. A análise de sentimentos a partir de tweets pode fornecer informações valiosas sobre como as companhias aéreas são percebidas no mercado.

O objetivo deste projeto foi realizar uma análise de sentimentos em tweets coletados sobre diferentes companhias aéreas. A análise precisava classificar os sentimentos dos tweets em três categorias: positivos, negativos e neutros. Além disso, foi necessário realizar uma Análise Exploratória de Dados (EDA) para extrair insights úteis sobre as percepções dos usuários.

Para isso, utilizei **Streamlit** para criar uma interface interativa que exibe os resultados da análise de sentimentos em tempo real. A etapa de EDA foi realizada utilizando as bibliotecas **pandas**, **numpy** e **matplotlib**, que permitiram a limpeza e manipulação dos dados, além da geração de gráficos e insights estatísticos. O processo envolveu:

1. Coleta de tweets sobre as companhias aéreas.
2. Classificação dos sentimentos com base em análise de texto.
3. Criação de gráficos interativos para visualizar a distribuição dos sentimentos e identificar padrões.

O resultado final foi um aplicativo interativo https://us-airline-sentiment.streamlit.app/ construído em **Streamlit**, onde os usuários podem visualizar os sentimentos relacionados a diferentes companhias aéreas. A ferramenta permite aos analistas obter insights rápidos sobre a percepção do público nas redes sociais, ajudando as empresas a monitorar sua imagem e melhorar sua estratégia de marketing e atendimento.

### Tecnologias Utilizadas
- **Streamlit**: Para criação da interface interativa.
- **pandas**: Para manipulação e análise de dados.
- **numpy**: Para cálculos numéricos e processamento de dados.
- **matplotlib**: Para visualização de dados e criação de gráficos.

## Como Rodar o Projeto

1. Clone o repositório para sua máquina local:

   ```bash
   git clone https://github.com/diogo-dantas/us-airline-sentiment.git
   cd us-airline-sentiment
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Execute o aplicativo Streamlit:

   ```bash
   streamlit run app.py
   ```

4. Acesse a interface no navegador.

## Contribuições
Sinta-se à vontade para contribuir para o projeto! Para sugestões, correções ou melhorias, abra um **issue** ou envie um **pull request**.

## Licença
Este projeto é licenciado sob a MIT License - consulte o arquivo [LICENSE](LICENSE) para mais detalhes.
