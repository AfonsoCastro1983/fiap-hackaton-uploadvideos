import boto3
import jwt
import json
import uuid

s3_client = boto3.client('s3')
dynamodb_client = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # Obter o token JWT do header Authorization
    token = event['headers']['Authorization'].split(" ")[1]
    body = event['body']

    # Decodificar o token JWT
    try:
        decoded_token = jwt.decode(
            token, 
            algorithms=["RS256"], 
            options={"verify_signature": False}
        )
        user_id = decoded_token['sub']
    except Exception as e:
        return {
            "statusCode": 401,
            "body": f"Token inválido: {str(e)}"
        }

    resposta = {
        id_user: user_id,
        resposta: 'Upload Concluído'
    }

    return {
        "statusCode": 200,
        "body": json.dumps(resposta)
    }