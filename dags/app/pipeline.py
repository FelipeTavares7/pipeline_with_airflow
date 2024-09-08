##################################################################################################
############################    Pipeline de Dados With Airflow    ################################
##################################################################################################

# Bibliotecas
from airflow import DAG # type: ignore
from airflow.operators.python import PythonOperator # type: ignore
from datetime import datetime
import pandas as pd
import os

# Função para carregar dados brutos nos formatos CSV para a camada Bronze.
def upload_raw_data_to_bronze():
    try:
        print("Iniciando a função upload_raw_data_to_bronze")
        
        # Caminho para o arquivo CSV de entrada
        input_file_path = os.path.join('input-data', 'raw_data.csv')
        print(f"Localização do arquivo de entrada: {input_file_path}")
        
        # Caminho para salvar o arquivo Parquet na camada Bronze
        bronze_output_path = os.path.join('layers/bronze', 'raw_data.parquet')
        print(f"Localização do arquivo de saída (Parquet): {bronze_output_path}")
        
        # Verifica se o arquivo de entrada existe
        if not os.path.exists(input_file_path):
            print(f"Erro: Arquivo de entrada não encontrado em {input_file_path}")
            return
        
        # Carrega os dados do CSV
        print("Carregando dados do CSV...")
        df = pd.read_csv(input_file_path)
        print(f"Dados carregados com sucesso. Total de linhas: {len(df)}")
        
        # Salva os dados como Parquet na camada Bronze
        print("Salvando dados no formato Parquet...")
        df.to_parquet(bronze_output_path, index=False)
        print(f"Dados salvos com sucesso em {bronze_output_path}")

    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

# Função para ler e limpar os dados da camada Bronze:
    # Remove registros com campos nulos (nome, email, data de nascimento).
    # Corrigie formatos de email inválidos. (para ser um email valido é necessário ter o carácter “@ˮ)
    # Calcula a idade dos usuários com base na data de nascimento.
# Salva na camada Silver
def process_bronze_to_silver():
    try:
        print("Iniciando a função process_bronze_to_silver")
        
        # Caminho para o arquivo Parquet na camada Bronze
        bronze_input_path = os.path.join('layers/bronze', 'raw_data.parquet')
        print(f"Localização do arquivo de entrada (Bronze): {bronze_input_path}")
        
        # Caminho para salvar o arquivo Parquet na camada Silver
        silver_output_path = os.path.join('layers/silver', 'transformed_data.parquet')
        print(f"Localização do arquivo de saída (Silver): {silver_output_path}")
        
        # Carrega os dados da camada Bronze
        print("Carregando dados da camada Bronze...")
        df = pd.read_parquet(bronze_input_path)
        print(f"Dados carregados com sucesso. Total de linhas: {len(df)}")
        
        # Contagem de nulos antes da limpeza
        null_count_before = df[['name', 'email', 'date_of_birth']].isnull().sum()
        print(f"Número de valores nulos antes da limpeza:\n{null_count_before}")
        
        # Remove registros com campos nulos em 'name', 'email' e 'date_of_birth'
        print("Removendo registros com campos nulos...")
        df_cleaned = df.dropna(subset=['name', 'email', 'date_of_birth'])
        print(f"Total de linhas após remoção de nulos: {len(df_cleaned)}")
        
        # Corrige formatos de email inválidos (verifica se contém '@')
        print("Corrigindo formatos de email inválidos...")
        df_cleaned = df_cleaned[df_cleaned['email'].str.contains('@')]
        print(f"Total de linhas após correção de emails inválidos: {len(df_cleaned)}")
        
        # Calcula a idade dos usuários
        print("Calculando a idade dos usuários...")
        df_cleaned['date_of_birth'] = pd.to_datetime(df_cleaned['date_of_birth'], errors='coerce')
        df_cleaned['age'] = (pd.Timestamp.now().year - df_cleaned['date_of_birth'].dt.year)
        
        # Contagem de nulos após a limpeza
        null_count_after = df_cleaned[['name', 'email', 'date_of_birth']].isnull().sum()
        print(f"Número de valores nulos após a limpeza:\n{null_count_after}")
        
        # Salva os dados limpos na camada Silver
        print("Salvando dados limpos na camada Silver...")
        df_cleaned.to_parquet(silver_output_path, index=False)
        print(f"Dados limpos salvos com sucesso em {silver_output_path}")

    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

# Função para ler e processar os dados da camada Prata.
    # Executa transformações adicionais:
        # Agrega os dados por faixa etária e status, facilitando análises demográficas e comportamentais.
        # Cria um dataset que mostra o número de usuários por faixa etária e por status.
# Salva os dados transformados na camada Gold, prontos para análise e uso em decisões estratégicas.
def process_silver_to_gold():
    try:
        print("Iniciando a função process_silver_to_gold")
        
        # Caminho para o arquivo Parquet na camada Silver
        silver_input_path = os.path.join('layers/silver', 'transformed_data.parquet')
        print(f"Localização do arquivo de entrada (Silver): {silver_input_path}")
        
        # Caminho para salvar o arquivo Parquet na camada Ouro
        gold_output_path = os.path.join('layers/gold', 'aggregated_data.parquet')
        print(f"Localização do arquivo de saída (Gold): {gold_output_path}")
        
        # Carrega os dados da camada Silver
        print("Carregando dados da camada Silver...")
        df = pd.read_parquet(silver_input_path)
        print(f"Dados carregados com sucesso. Total de linhas: {len(df)}")
        
        # Cria faixa etária
        print("Criando faixa etária...")
        bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        labels = ['0-10', '11-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '81-90', '91-100']
        df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels, right=False)
        
        # Agrega dados por faixa etária e status
        print("Agregando dados por faixa etária e status...")
        aggregated_data = df.groupby(['age_group', 'subscription_status']).size().reset_index(name='user_count')
        print(f'Verificando df final...\n', aggregated_data.head())
        
        # Salva dados agregados na camada Ouro
        print("Salvando dados agregados na camada Ouro...")
        aggregated_data.to_parquet(gold_output_path, index=False)
        print(f"Dados agregados salvos com sucesso em {gold_output_path}")

    except Exception as e:
        print(f"Erro ao processar os dados: {e}")

# DAG
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 9, 6),
    'retries': 1,
}

with DAG(
    dag_id='data_pipeline',
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
) as dag:

    # Tasks
    upload_task = PythonOperator(
        task_id='upload_raw_data_to_bronze_task',
        python_callable=upload_raw_data_to_bronze,
    )
    
    process_bronze_to_silver_task = PythonOperator(
        task_id='process_bronze_to_silver_task',
        python_callable=process_bronze_to_silver,
    )
    
    process_silver_to_gold_task = PythonOperator(
        task_id='process_silver_to_gold_task',
        python_callable=process_silver_to_gold,
    )

    # Define a ordem das tarefas
    upload_task >> process_bronze_to_silver_task >> process_silver_to_gold_task
