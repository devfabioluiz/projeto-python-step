
from django import template

register = template.Library()

@register.filter(name='format_moeda')
def format_moeda(valor):
    """Formata um número como moeda brasileira: 1999.9 → R$ 1.999,90"""
    try:
        valor = float(valor)
        inteiro = int(valor)
        centavos = int(round((valor - inteiro) * 100))

        # Formata parte inteira com separador de milhar
        parte_inteira = f"{inteiro:,}".replace(",", ".")

        if centavos == 0:
            return f"R$ {parte_inteira},00"
        elif centavos < 10:
            return f"R$ {parte_inteira},0{centavos}"
        else:
            return f"R$ {parte_inteira},{centavos}"
    except (ValueError, TypeError):
        return "R$ 0,00"


@register.filter(name='label_status')
def label_status(estoque):
    """Retorna um badge HTML baseado na quantidade em estoque"""
    try:
        estoque = int(estoque)
    except (ValueError, TypeError):
        estoque = 0

    if estoque == 0:
        return '<span class="badge badge-danger">Indisponível</span>'
    elif estoque <= 5:
        return f'<span class="badge badge-warning">Apenas {estoque} un.</span>'
    else:
        return f'<span class="badge badge-success">{estoque} un.</span>'
          