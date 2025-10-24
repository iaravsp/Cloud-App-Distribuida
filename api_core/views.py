from django.shortcuts import render
# Create your views here.

import requests
import json

import os
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import SavedImage

PEXELS_BASE_URL = "https://api.pexels.com/v1/"


def criar_headers():
    """Cria os headers HTTP necessários, usando a chave Pexels das configurações."""
    # settings.PEXELS_API_KEY deve ser configurada em settings.py a partir das variáveis de ambiente
    api_key = getattr(settings, 'PEXELS_API_KEY', None)
    if not api_key:
        return None
    return {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }

# 1. FUNÇÃO 'UPLOAD' (Busca na Pexels e Salva no DB)
@csrf_exempt
def upload_image(request):
    """Realiza a busca de uma imagem (exemplo: 'cloud') e salva os metadados."""
    if request.method != 'POST':
        return JsonResponse({"message": "Método não permitido"}, status=405)

    headers = criar_headers()
    if headers is None:
        return JsonResponse({"message": "Erro de configuração: Chave Pexels ausente."}, status=500)

    # Você pode extrair o termo de busca do corpo da requisição POST, ou usar um padrão
    search_term = "cabelo" 

    try:
        endpoint = PEXELS_BASE_URL + f"search?query={search_term}&per_page=1"
        response = requests.get(endpoint, headers=headers)
        response.raise_for_status()

        data = response.json()
        if data.get("photos"):
            photo = data["photos"][0]
            
            # 1. Salvar no Banco de Dados
            SavedImage.objects.create(
                pexels_id=photo.get("id"),
                photographer=photo.get("photographer"),
                tags=search_term, # Simplificação: salva o termo de busca como tag
                original_url=photo.get("src", {}).get("original")
            )

            return JsonResponse({"message": "Imagem e metadados salvos com sucesso.", "id": photo.get("id")}, status=200)
                
        return JsonResponse({"message": "Nenhuma imagem encontrada."}, status=404)

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        return JsonResponse({"message": f"Erro na API Pexels: {status_code}"}, status_code)
    except Exception as e:
        return JsonResponse({"message": f"Erro interno ao processar: {str(e)}"}, status=500)

# 2. FUNÇÃO 'LISTAR' (Busca as Tags Salvas no DB)
def list_tags(request):
    """Lista todas as tags de imagens salvas no banco de dados."""
    if request.method != 'GET':
        return JsonResponse({"message": "Método não permitido"}, status=405)
    tags = SavedImage.objects.values_list('tags', flat=True).distinct()
    return JsonResponse({"tags": list(tags), "count": len(tags)}, status=200)

    # """Apresenta as tags de todas as imagens salvas no DB."""
    # if request.method != 'GET':
    #     return JsonResponse({"message": "Método não permitido"}, status=405)
    
    # # Busca todas as tags
    # tags = SavedImage.objects.values_list('tags', flat=True).distinct()
    
    # # Processa as tags (se tiverem múltiplas separadas por vírgula) e remove duplicatas
    # all_tags = set()
    # for tag_list in tags:
    #     for tag in tag_list.split(','):
    #         all_tags.add(tag.strip())
            
    # return JsonResponse({"tags": list(all_tags), "count": len(all_tags)}, status=200)


# 3. FUNÇÃO 'MOSTRAR' (Exibe o Link da Imagem Salva)
def show_image(request, image_id):
    """Exibe a imagem selecionada (ou seu link) a partir do ID salvo."""
    if request.method != 'GET':
        return JsonResponse({"message": "Método não permitido"}, status=405)
        
    try:
        image = SavedImage.objects.get(pexels_id=image_id)
        
        # Opção 1: Retorna a URL para o cliente exibir
        return JsonResponse({
            "image_id": image.pexels_id,
            "photographer": image.photographer,
            "image_url": image.original_url
        }, status=200)

        # Opção 2: Redireciona o usuário diretamente para a imagem (se quiser exibir no navegador)
        # return redirect(image.original_url) 
        
    except SavedImage.DoesNotExist:
        return JsonResponse({"message": "Imagem não encontrada no banco de dados."}, status=404)