#from email.mime import image
from hashlib import blake2b
from pickletools import optimize
from re import T
from tabnanny import verbose
from django.db import models
from PIL import Image
import os
from django.conf import settings
# Create your models here.
from django.utils.text import slugify


class Produto(models.Model):
    nome = models.CharField(max_length=255)
    curt_descrition = models.TextField(max_length=255)
    long_descrition = models.TextField()
    imagem = models.ImageField(
        upload_to='product_images/%Y/%m', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    cost_marketing = models.FloatField(verbose_name='Cost')
    cost_marketing_promotion = models.FloatField(
        default=0, verbose_name='Promotion Cost')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    def get_cost_formated(self):
        return f'R$ {self.cost_marketing:.2f}'.replace('.', ',')

    get_cost_formated.short_description = 'Cost'

    def get_cost_promotion_formated(self):
        return f'R$ {self.cost_marketing_promotion:.2f}'.replace('.', ',')

    get_cost_promotion_formated.short_description = 'Promotion Cost'

    @staticmethod
    def resize_image(imagens, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, imagens.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            img_pil.close
            return

        new_height = round((new_width * original_height) / original_width)
        print('teste................')
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)

        new_img.save(img_full_path,
                     optimize=True,
                     quality=50)

    def save(self, *args, **kwargs):

        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:

            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variações'
        verbose_name_plural = 'Variações'
