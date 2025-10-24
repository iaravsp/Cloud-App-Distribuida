from django.db import models

# Create your models here.

class SavedImage(models.Model):
    """
    Modelo para armazenar metadados de imagens salvas da Pexels.
    """
    # O 'id' do Django será a chave primária, mas mantemos o ID da Pexels
    pexels_id = models.CharField(max_length=50, db_index=True)
    
    photographer = models.CharField(max_length=255)
    
    # Armazenamos as tags como um campo de texto ou ArrayField (se suportado pelo DB)
    tags = models.TextField(help_text="Tags associadas à imagem (separadas por vírgula)")
    
    # URL da imagem original (link que será exibido)
    original_url = models.URLField(max_length=500)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image ID: {self.pexels_id} by {self.photographer}"