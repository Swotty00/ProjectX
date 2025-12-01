from datasets import Dataset

def tokenize_dataset(df:Dataset, tokenizer) -> Dataset:
    hf_dataset = Dataset.from_pandas(df, preserve_index=False)

    # Mapeia os labels para binário
    def encode_labels(df:Dataset):
        df['label'] = 1 if df['label'] == 'positive' else 0
        return df

    def tokenize_function(df):
        return tokenizer(df['texto'], 
                         padding="max_length", 
                         truncation=True, 
                         max_length=128) # verificar média de tokens dentro do dataset para poder escolher o tamaho ideal

    # Aplica o mapeamento de labels
    hf_dataset = hf_dataset.map(encode_labels)

    # Tokeniza diversas frases ao mesmo tempo (aula de arquivos)
    tokenized_datasets = hf_dataset.map(tokenize_function, 
                                        batched=True)

    tokenized_datasets = tokenized_datasets.remove_columns(["texto"])

    return tokenized_datasets
