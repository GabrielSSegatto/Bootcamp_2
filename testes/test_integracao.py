import pytest
from services import CEPService

def test_viacep_integracao_real():
    # Usando o CEP do UniCEUB que você colocou no seed
    dados = CEPService.buscar_endereco("70790075")
    
    assert dados is not None
    assert dados['localidade'] == "Brasília"
    assert "logradouro" in dados
    assert dados['uf'] == "DF"