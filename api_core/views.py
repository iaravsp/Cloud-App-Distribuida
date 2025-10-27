import requests
import json
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import SavedImage

PEXELS_BASE_URL = "https://api.pexels.com/v1/"


def criar_headers():
    """Cria os headers HTTP necessários, usando a chave Pexels das configurações."""
    api_key = getattr(settings, 'PEXELS_API_KEY', None)
    if not api_key:
        return None
    return {
        "Authorization": api_key,
        "Content-Type": "application/json"
    }


@csrf_exempt
def upload_image(request):
    """Realiza a busca de uma imagem (termo enviado via JSON) e salva os metadados."""
    if request.method != 'POST':
        return JsonResponse({"message": "Método não permitido"}, status=405)

    headers = criar_headers()
    if headers is None:
        return JsonResponse({"message": "Erro de configuração: Chave Pexels ausente."}, status=500)

    try:
        body = {}
        if request.body:
            try:
                body = json.loads(request.body.decode('utf-8'))
            except Exception:
                body = {}
    except Exception:
        body = {}

    search_term = (body.get('term') or body.get('search_term') or body.get('query') or '').strip()

    try:
        # Use params para evitar problemas com encoding de query
        endpoint = PEXELS_BASE_URL + "search"
        response = requests.get(endpoint, headers=headers, params={"query": search_term, "per_page": 1})
        response.raise_for_status()

        data = response.json()
        if data.get("photos"):
            photo = data["photos"][0]
            pexels_id_str = str(photo.get("id"))

            # Evita criar duplicatas: se já existe um SavedImage com esse pexels_id,
            # retornamos o registro existente em vez de criar outro.
            existing = SavedImage.objects.filter(pexels_id=pexels_id_str).order_by('-created_at').first()
            if existing:
                return JsonResponse({"message": "Imagem já existe.", "id": existing.pexels_id}, status=200)

            # 1. Salvar no Banco de Dados
            SavedImage.objects.create(
                pexels_id=pexels_id_str,
                photographer=photo.get("photographer"),
                tags=search_term, # Simplificação: salva o termo de busca como tag
                original_url=photo.get("src", {}).get("original")
            )

            return JsonResponse({"message": "Imagem e metadados salvos com sucesso.", "id": pexels_id_str}, status=200)

        return JsonResponse({"message": "Nenhuma imagem encontrada."}, status=404)

    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        return JsonResponse({"message": f"Erro na API Pexels: {status_code}"}, status_code)
    except Exception as e:
        return JsonResponse({"message": f"Erro interno ao processar: {str(e)}"}, status=500)

def list_tags(request):
    """Lista todas as tags de imagens salvas no banco de dados."""
    if request.method != 'GET':
        return JsonResponse({"message": "Método não permitido"}, status=405)
    tags = SavedImage.objects.values_list('tags', flat=True).distinct()
    return JsonResponse({"tags": list(tags), "count": len(tags)}, status=200)


@csrf_exempt
def show_image(request, image_id):
    """Exibe a imagem selecionada (ou seu link) a partir do ID salvo."""
    if request.method != 'GET':
        return JsonResponse({"message": "Método não permitido"}, status=405)
        
    try:
        image = SavedImage.objects.filter(pexels_id=image_id).order_by('-created_at').first()
        if not image:
            return JsonResponse({"message": "Imagem não encontrada no banco de dados."}, status=404)

        tags_list = [t.strip() for t in (image.tags or '').split(',') if t.strip()]
        return JsonResponse({
            "id": image.pexels_id,
            "photographer": image.photographer,
            "url": image.original_url,
            "tags": tags_list,
            "created_at": image.created_at.isoformat()
        }, status=200)
        
    except SavedImage.DoesNotExist:
        return JsonResponse({"message": "Imagem não encontrada no banco de dados."}, status=404)

@csrf_exempt
def list_images(request):

    if request.method != 'GET':
        return JsonResponse({"message": "Método não permitido"}, status=405)

    images_qs = SavedImage.objects.all().order_by('-created_at')
    images = []
    for img in images_qs:
        tags_list = [t.strip() for t in (img.tags or '').split(',') if t.strip()]
        images.append({
            "id": img.pexels_id,
            "photographer": img.photographer,
            "url": img.original_url,
            "tags": tags_list,
            "created_at": img.created_at.isoformat()
        })

    return JsonResponse({"images": images, "count": len(images)}, status=200)