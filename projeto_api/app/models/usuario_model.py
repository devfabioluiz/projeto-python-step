from app.database.supabase_client import supabase_request


def listar_usuarios():
    response = supabase_request(
        "rest/v1/usuarios?select=*",
        method="GET",
    )
    if response.status_code != 200:
        raise Exception(f"Erro ao listar usuÃ¡rios: {response.text}")
    return response.json()


def criar_usuario(nome):
    response = supabase_request(
        "rest/v1/usuarios",
        method="POST",
        data={"nome": nome},
    )
    if response.status_code not in (200, 201):
        raise Exception(f"Erro ao criar usuÃ¡rio: {response.text}")
    return response.json()
