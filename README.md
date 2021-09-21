# Arquitetura Batch

Arquitetura batch de uma plataforma de ML usando componentes da AWS.

Esse projeto visa simular o funcionamento a etapa 7 a partir da fila batch proposto na arquitetura batch [clique aqui](https://github.com/pamfidelis/arquitetura-batch-case/blob/main/docs/arquitetura_batch.png)


## Guia

### Pré requisitos
Para execução do projeto localmente é necessário ter o ambiente previamente configurado:

### Instalação do software

```
Docker 
```

#### Configuração das credenciais da AWS
* [Consulte aqui como configurar.](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html)

#### Fila SQS
Configuração da fila:
    * Nome:  arq-batch-sqs

### S3
* Configurações do bucket:
    * Nome: arq-batch-s3


### Instalação e execução
```
docker build \
-t pamfidelis/arq-batch-aws \
--build-arg AWS_ACCESS_KEY_ID=$(echo $AWS_ACCESS_KEY_ID) \
--build-arg AWS_SECRET_ACCESS_KEY=$(echo $AWS_SECRET_ACCESS_KEY) \
--build-arg AWS_DEFAULT_REGION=$(echo $AWS_DEFAULT_REGION) \
--no-cache .


docker run pamfidelis/arq-batch-aws
```

### Estrutura de pastas

    config: contém um arquivo yaml com as configurações do projeto
    data: 
        input: usada para download do dataset de entrada
        output: resultado do modelo
    docs: contém a arquitetura batch completa
    model: código do modelo
    src: 
        main.py código principal de execução
        s3.py - classe que se conecta no S3
        sqs.py - classe que se conecta no SQS
    utils: contém códigos auxiliares para execução:
        train_model.py - script usado para treino de um modelo dumb
        config.py: fazer load do arquivo de ocnfiguração
        mock_process.py: passo a passo simulando as etapas  1, 2 e 3
        send_message.py: simula a etapa 3, onde é enviado o evento para a fila

## Backlog
* Alterar a forma de download e upload dos arquivos para que sejam salvos em memória;
* Melhorar a forma como os logs são lançados;
* Transformar a arquitetura em streaming;
* Fazer a tratativa do método receive_message() da classe SQSQueue() para lidar com fila vazia;
* Automatizar a criação de bucket e da fila

## Referencias
* [Dataset usado](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) 
* [Modelo de Regressão Linear exemplo](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) 
