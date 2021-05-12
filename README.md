# Case - Arquitetura Batch

Arquitetura batch de uma plataforma de ML usando componentes da AWS.

Esse projeto visa simular o funcionamento a etapa 7 a partir da fila batch proposto na arquitetura batch.

## Guia

### Pré requisitos

Para execução do projeto localmente é necessário ter o ambiente previamente configurado:
* Instalação dos seguintes softwares

```
Docker 
Python - versão 3.8.5
```

* Confguração as credencias da AWS. [Consulte aqui como configurar.](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html)
* Ter uma fila SQS
* Ter um bucket no S3.


### Estrutura de pastas

    config: contém um arquivo yaml com as configurações do projeto
    data: usada para download dos arquivos necessários para execução
    docs: contém a arquitetura batch completa
    model: código do modelo
    src: código principal de execução
    utils: contém códigos auxiliares para execução:
        s3.py - classe que se conecta no S3
        sqs.py - classe que se conecta no SQS
        train_model.py - script usado para treino de um modelo dumb, geração de um pickle e envio para um bucket no S3

## Backlog
* Alterar a forma de download e upload dos arquivos para que sejam salvos em memória;
* Melhorar a forma como os logs são lançados;
* Transformar a arquitetura em streaming;
* Fazer a tratativa do método receive_message() da classe SQSQueue() para lidar com fila vazia;

## Referencias
* [Dataset usado](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) 
* [Modelo de Regressão Linear exemplo](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html) 
