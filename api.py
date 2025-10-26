from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
import requests

# 1. Configuração da Aplicação FastAPI
app = FastAPI(
    title="API de Busca de URL",
    description="Uma API que recebe um link via POST e retorna o conteúdo do link."
)

# 2. Definição do Modelo de Dados (Corpo da Requisição)
# Usamos Pydantic para garantir que o corpo do POST tenha um campo 'link'
class LinkRequest(BaseModel):
    # HttpUrl garante que o valor é uma URL válida
    link: HttpUrl

# 3. Endpoint POST para buscar o link
@app.post("/buscar-link/")
def buscar_link_endpoint(request_body: LinkRequest):
    """
    Recebe um link no corpo da requisição (JSON) e retorna 
    o conteúdo HTML/texto do link.
    """
    
    url = str(request_body.link) # Converte o Pydantic HttpUrl para string
    
    try:
        # Faz uma requisição GET para a URL
        # Define um timeout para evitar que a requisição demore demais
        response = requests.get(url, timeout=10)
        
        # Verifica se o status code é de sucesso (200 OK)
        response.raise_for_status() 
        
        # Retorna o conteúdo da URL como texto.
        # Você pode querer limitar o tamanho do retorno para evitar sobrecarga.
        return {
            "link_original": url,
            "status_code": response.status_code,
            "tamanho_conteudo": len(response.text),
            "conteudo_parcial": response.text[:2000] # Retorna os primeiros 2000 caracteres
        }

    except requests.exceptions.RequestException as e:
        # Captura erros de rede, timeout, ou status codes 4xx/5xx
        raise HTTPException(
            status_code=400, 
            detail=f"Falha ao buscar a URL: {e}"
        )

# 4. Endpoint GET simples para verificar se a API está funcionando
@app.get("/")
def health_check():
    return {"status": "ok", "message": "A API está funcionando."}
