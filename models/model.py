import sys
from pathlib import Path #rever

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from transformers import BertTokenizer, BertForSequenceClassification
from transformers import TrainingArguments
from transformers import Trainer
from src.db import connector
import pandas as pd
from dotenv import load_dotenv
from models import tokenizer

OUTPUT_PATH = Path('./results')
LOGS_PATH = Path('./logs')

def get_dataset_from_db(conn):
    sql_query = "SELECT texto, label FROM reviews;"

    try:
        df = pd.read_sql_query(sql_query, conn)
        print(f"Dataset carregado do DB. Total de registros: {len(df)}")
        return df
        
    except Exception as e:
        print(f"Erro ao carregar dados do DB: {e}")
        return pd.DataFrame() # Retorna DataFrame vazio em caso de erro

def get_training_args(num_train_epochs:int, per_device_train_batch_size:int, per_device_eval_batch_size:int, warmup_steps:int, weight_decay:int, logging_steps:int):
    training_args = TrainingArguments(
        output_dir=OUTPUT_PATH,
        num_train_epochs=num_train_epochs,
        per_device_train_batch_size=per_device_train_batch_size,
        per_device_eval_batch_size=per_device_eval_batch_size,
        warmup_steps=warmup_steps,
        weight_decay=weight_decay,
        logging_dir=LOGS_PATH,
        logging_steps=logging_steps,
    )

    return training_args

def get_trainer(model, tokenizer, train_dataset, eval_dataset):
    training_args = get_training_args(3, 8, 8, 500, 0.01, 10)

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=eval_dataset,
    )
    
    return trainer


load_dotenv()
conn = connector.connect_db()

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

df = get_dataset_from_db(conn)
tokenized_data = tokenize_dataset(df, tokenizer)
train_test_split = tokenized_data.train_test_split(test_size = 0.1)

train_dataset = train_test_split['train']
eval_dataset = train_test_split['test']


trainer.train()
trainer.save_model("best-model/")

connector.disconnect_db(conn)



def load_pretrained_model(pretrained_config:str)->BertForSequenceClassification:
    model = BertForSequenceClassification.from_pretrained(pretrained_config)
    return model



load_pretrained_model('bert-base-uncased')
