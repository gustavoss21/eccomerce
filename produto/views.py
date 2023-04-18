from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from . import models
from django.contrib import messages
from utils import utils
from perfil.models import Perfil

# Create your views here.


class ListaProduto(ListView):
    model = models.Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 10


class DetalheProduto(DetailView):
    model = models.Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'


class AdicionarAoCarrinho(View):
    def get(self, *args, **kwargs):
        '''if self.request.session.get('carrinho'):
            del self.request.session['carrinho']
            self.request.session.save()'''
        http_referer = self.request.META.get('HTTP_REFERER',
                                             reverse('produto:lista'))

        variacao_id = self.request.GET.get('vi')

        if not variacao_id:
            messages.error(self.request,
                           'produto não existe')

            return redirect(http_referer)
        variacao = get_object_or_404(models.Variacao, id=variacao_id)

        produto = variacao.produto
        variacao_estoque = variacao.estoque

        produto_id = variacao.id
        produto_nome = variacao.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        Carrinho = self.request.session['carrinho']

        if variacao_id in Carrinho:

            quantidade_carrinho = Carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            if variacao_estoque < quantidade_carrinho:
                messages.warning(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no '
                    f'produto "{produto_nome}". Adicionamos {variacao_estoque}x '
                    f'no seu carrinho'
                )
                quantidade_carrinho = variacao_estoque
            Carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            Carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho
            Carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * \
                quantidade_carrinho
        else:

            Carrinho[variacao_id] = {
                'produto_id': produto_id,
                'produto_nome': produto_nome,
                'variacao_nome': variacao_nome,
                ' variacao_id': variacao_id,
                'preco_unitario': preco_unitario,
                'preco_unitario_promocional': preco_unitario_promocional,
                'preco_quatitativo': preco_unitario,
                'preco_quatitativo_promocional': preco_unitario_promocional,
                'quantidade': 1,
                'slug': slug,
                'imagem': imagem
            }

        self.request.session.save()
        messages.success(self.request, f'Produto {produto_nome} {variacao_nome} adicionado ao seu '
                         f'carrinho {Carrinho[variacao_id]["quantidade"]}x.')
        return redirect(http_referer)


class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get('HTTP_REFERER',
                                             reverse('produto:lista'))

        variacao_id = self.request.GET.get('vid')

        if not variacao_id:

            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        carrinho = self.request.session['carrinho'][variacao_id]

        messages.success(
            self.request,
            f'Produto {carrinho["produto_nome"]}'
            f'removido do seu carrinho'
        )
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        variacao_id = self.request.GET.get('vid')
        return HttpResponse('RemoverDoCarrinho')


class Carrinho(View):
    def get(self, *args, **kwargs):

        return render(self.request, 'produto/carrinho.html')


class ResumoDaCompra(ListView):

    def get(self, *args, **kwargs):

        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()

        if not perfil:
            messages.error(
                self.request,
                'Usuario sem perfil.'
            )
            return redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'Carrinho vazio'
            )
            return redirect('produto:lista')

        context = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
        }

        return render(self.request, 'produto/resumodacompra.html', context)
