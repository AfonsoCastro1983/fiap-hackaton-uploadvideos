import boto3
import jwt
import json
import uuid
import os
from datetime import datetime
from urllib.parse import parse_qs

s3_client = boto3.client('s3',aws_access_key_id=os.getenv('va_aws_key_id'),aws_secret_access_key=os.getenv('va_aws_key_secret'))
dynamodb_client = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Obter o token JWT do header Authorization
    token = event['headers']['Authorization'].split(" ")[1]
    body = event['body']
    print('token', token)
    print('body', body)

    # Decodificar os dados do formato x-www-form-urlencoded
    form_data = parse_qs(body)
    # Obter o valor do campo 'nome_arquivo'
    nome_arquivo = form_data.get('nome_arquivo', [None])[0]

    # Gerando IDs
    video_id = str(uuid.uuid4())
    bucket_name = "amz.video-upload.bucket"

    # Decodificar o token JWT
    try:
        decoded_token = jwt.decode(
            token, 
            algorithms=["RS256"], 
            options={"verify_signature": False}
        )
        user_id = decoded_token['sub']
        cognito_name = decoded_token['cognito:username']
        name = decoded_token['name']
        email = decoded_token['email']
    except Exception as e:
        return {
            "statusCode": 401,
            "body": f"Token inválido: {str(e)}"
        }

    presigned_url_s3 = s3_client.generate_presigned_url(
        'put_object',
        Params={'Bucket': bucket_name, 'Key': f'videos/{video_id}/{nome_arquivo}'},
        ExpiresIn=3600
    )

    # Adicionando data e hora
    timestamp = datetime.utcnow().isoformat()

    retorno = {
        "user": {
            "userId":user_id,
            "cognito_name": cognito_name,
            "name": name,
            "email": email
        },
        "videoId": video_id,
        "videoName": nome_arquivo,
        "timestamp": timestamp,
        "s3_key": f'videos/{video_id}/{nome_arquivo}',
        "presigned_url": presigned_url_s3
    }

    # Salvando no DynamoDB
    table = dynamodb_client.Table("VideosTable")
    table.put_item(
        Item=retorno
    )

    return {
        "statusCode": 200,
        "body": json.dumps(retorno)
    }