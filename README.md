# Pipeline de Dados com Apache Airflow

Este projeto configura um pipeline de dados utilizando o Apache Airflow para processar e transformar dados em diferentes camadas: Bronze, Prata e Ouro.

## Estrutura do Projeto

- **input-data/**: Pasta contendo arquivos de entrada no formato CSV.
- **layers/**: Pasta com as camadas de armazenamento dos dados:
  - **bronze/**: Camada para armazenar os dados brutos no formato Parquet.
  - **silver/**: Camada para armazenar os dados limpos e transformados.
  - **gold/**: Camada para armazenar os dados agregados e prontos para análise.
- **dags/**: Pasta contendo os arquivos Python com as definições das DAGs do Airflow.
  - **pipeline.py**: Arquivo contendo todas as etapas do pipeline de dados, incluindo carregamento, limpeza e transformação dos dados.

## Funcionalidade

1. **Camada Bronze**
   - **Objetivo**: Carregar dados brutos do arquivo CSV para a camada Bronze.
   - **Função**: `upload_raw_data_to_bronze`
   - **Descrição**: Carrega o arquivo CSV e o converte para o formato Parquet na pasta `layers/bronze`.

2. **Camada Prata**
   - **Objetivo**: Limpar e transformar os dados da camada Bronze.
   - **Função**: `transform_bronze_to_silver`
   - **Descrição**: Remove registros com campos nulos, corrige formatos de e-mail inválidos e calcula a idade dos usuários. Os dados limpos são salvos na camada `layers/silver`.

3. **Camada Ouro**
   - **Objetivo**: Agregar e preparar os dados para análise.
   - **Função**: `process_silver_to_gold`
   - **Descrição**: Agrupa os dados por faixa etária e status, e salva os dados agregados na camada `layers/gold`.

## Configuração

1. **Instalação do Docker e Docker Compose**
   - Certifique-se de ter o Docker e o Docker Compose instalados em sua máquina.

2. **Construção e Execução**
   - No diretório raiz do projeto, execute os comandos:
     ```bash
     docker build -t pipeline_with_airflow .
     ```
     ```bash
     docker compose up
     ```

3. **Acessar o Airflow**
   - Acesse a interface do Airflow através do navegador em [http://localhost:8080](http://localhost:8080).
   - Ative e execute a DAG chamada `pipeline`.

## Logs

- Os logs das tarefas podem ser visualizados na interface do Airflow.
- Certifique-se de verificar os logs para garantir que todas as etapas do pipeline foram concluídas com sucesso.
- Foram introduzidos vários `prints` para facilitar acompanhamento de cada passo.

## Considerações Finais

Este projeto foi desenvolvido para demonstrar o uso do Apache Airflow para orquestração de pipeline de dados e pode ser ajustado para diferentes casos de uso conforme necessário.
