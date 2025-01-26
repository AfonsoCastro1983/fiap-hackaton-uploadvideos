# Lambda para Geração de URLs Pre-assinadas no Amazon S3

## Introdução

Este projeto implementa uma função AWS Lambda para:
- Gerar URLs pre-assinadas do Amazon S3 para upload de vídeos.
- Decodificar e validar tokens JWT fornecidos pelo Amazon Cognito.
- Registrar metadados do upload em uma tabela DynamoDB.

O objetivo é demonstrar como integrar serviços da AWS, como **Amazon S3**, **Amazon Cognito** e **Amazon DynamoDB**, para construir soluções seguras e escaláveis de gerenciamento de uploads.

---

## Funcionalidades

1. **Geração de URLs Pre-assinadas**:
   - Cria URLs para uploads diretos ao Amazon S3 com tempo de expiração configurável.

2. **Validação de Tokens JWT**:
   - Decodifica e valida informações de autenticação dos usuários.

3. **Registro de Metadados no DynamoDB**:
   - Armazena informações sobre o upload, incluindo ID do vídeo, nome do arquivo, timestamp, e dados do usuário.

---

## Pré-requisitos

1. **Configuração do Amazon S3**:
   - Bucket chamado `amz.video-upload.bucket` configurado para aceitar uploads.

2. **Configuração do DynamoDB**:
   - Uma tabela chamada `VideosTable` com os seguintes atributos:
     - **Partition Key:** `userId` (String).
     - **Atributos adicionais:** `videoId`, `videoName`, `timestamp`, `s3_key`, `user_data`.

3. **Configuração do Cognito**:
   - Um User Pool configurado para autenticação e fornecimento de tokens JWT.

4. **Permissões IAM**:
   - A função Lambda deve ter permissões para:
     - Leitura e escrita no Amazon S3.
     - Acesso ao DynamoDB.

5. **Configuração de variáveis de ambiente**:
   - `va_aws_key_id`: Chave de acesso AWS.
   - `va_aws_key_secret`: Chave secreta de acesso AWS.

---

## Estrutura do Código

### Principais Componentes

1. **Decodificação do Token JWT**  
   O token JWT é obtido do cabeçalho Authorization e decodificado para extrair informações do usuário (ID, nome, e-mail, etc.).

2. **Geração de URL Pre-assinada**  
   Utiliza o cliente do Amazon S3 para criar uma URL pre-assinada que permite o upload seguro do vídeo.

3. **Registro no DynamoDB**  
   Os metadados do upload, incluindo informações do usuário, ID do vídeo e timestamp, são armazenados na tabela `VideosTable`.

4. **Retorno da Função**  
   A função retorna um JSON com informações detalhadas, incluindo a URL pre-assinada e os dados registrados.

---

## Configuração e Deploy

### 1. **Configuração do AWS Lambda**
- Crie uma nova função Lambda no console AWS.
- Suba o código como arquivo `.zip` ou utilizando um IDE compatível.
- Configure as variáveis de ambiente:
  ```plaintext
  va_aws_key_id=<sua-chave-de-acesso>
  va_aws_key_secret=<sua-chave-secreta>
  ```
- Vincule uma função IAM com permissões apropriadas.

### 2. **Configuração do Amazon S3**
- Crie um bucket chamado `amz.video-upload.bucket`.
- Garanta que o bucket aceite uploads autenticados.

### 3. **Configuração do DynamoDB**
- Crie uma tabela chamada `VideosTable` com os atributos mencionados nos pré-requisitos.

### 4. **Integração com Cognito**
- Configure um User Pool e ajuste as permissões para incluir o token JWT como cabeçalho em chamadas autenticadas.

---

## Fluxo de Funcionamento

1. **Requisição para Upload**:
   - O cliente envia uma requisição autenticada para a função Lambda com o nome do arquivo.

2. **Geração de URL Pre-assinada**:
   - A Lambda valida o token JWT e gera uma URL pre-assinada para o upload no Amazon S3.

3. **Registro no DynamoDB**:
   - As informações do upload são salvas na tabela `VideosTable`.

4. **Resposta ao Cliente**:
   - A função retorna uma resposta JSON contendo a URL pre-assinada e os metadados do upload.

---

## Exemplo de Resposta

### Resposta Bem-Sucedida:
```json
{
  "userId": "abc123",
  "user_data": {
    "cognito_name": "user_test",
    "name": "Test User",
    "email": "test.user@example.com"
  },
  "videoId": "550e8400-e29b-41d4-a716-446655440000",
  "videoName": "meu_video.mp4",
  "timestamp": "2025-01-01T00:00:00Z",
  "s3_key": "videos/550e8400-e29b-41d4-a716-446655440000/meu_video.mp4",
  "presigned_url": "https://amz.video-upload.bucket.s3.amazonaws.com/videos/550e8400-e29b-41d4-a716-446655440000/meu_video.mp4?AWSAccessKeyId=..."
}
```

### Erro de Token Inválido:
```json
{
  "statusCode": 401,
  "body": "Token inválido: assinatura inválida"
}
```

---

## Diagrama da Arquitetura

```plaintext
[ Cliente ] -> [ Lambda Function ] -> [ S3 Bucket ]
                            ↸         ↶
                        [ Cognito ]  [ DynamoDB ]
```

---

## Pontos de Aprendizado

- Uso de URLs pre-assinadas para uploads seguros no Amazon S3.
- Decodificação de tokens JWT para autenticação.
- Integração de serviços AWS para soluções escaláveis e seguras.

---

**Apresentação prática:** Durante a demonstração, o fluxo de geração de URL pre-assinada, validação de token e registro no DynamoDB será exibido em tempo real.