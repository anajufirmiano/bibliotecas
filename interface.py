"""
MÓDULO DE INTERFACE E COLETA DE DADOS (interface.py)
Alias para funcaocoleta.py para compatibilidade total.
"""

from .funcaocoleta import (
    lin,
    exibir_cabecalho,
    pedir_sexo,
    pedir_estado_civil,
    pedir_data_nascimento,
    pedir_cpf,
    pedir_endereco,
    pedir_telefone,
    pedir_cartao,
    exibir_menu_navegacao,
)

__all__ = [
    'lin',
    'exibir_cabecalho',
    'pedir_sexo',
    'pedir_estado_civil',
    'pedir_data_nascimento',
    'pedir_cpf',
    'pedir_endereco',
    'pedir_telefone',
    'pedir_cartao',
    'exibir_menu_navegacao',
]
