from re import T


def formata_preco(val):
    # return f'R$ {val:.2f}'.replace('.', ',')
    return val


def cart_total_qtd(carrinho):
    ts = 0
    for c in carrinho.values():
        ts += c['quantidade']
    return ts


def cart_totais(carrinho):
    total = 0

    for c in carrinho.values():

        if c.get('preco_quantitativo_promocional'):
            total += c.get('preco_quantitativo_promocional')

        elif c.get('preco_quantitativo'):
            total += c.get('preco_quantitativo')
    return total
