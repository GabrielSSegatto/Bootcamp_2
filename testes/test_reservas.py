import pytest
from app import app
from models import db, User, Evento, Sala, Sessao, Assento, Reserva
from datetime import datetime, timedelta


@pytest.fixture
def client():
    """Fixture que retorna um cliente de teste com banco em memória"""
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def setup_data():
    """Fixture que cria dados de teste"""
    # Criar sala
    # Criar sala (Arrumado pelo Caramez: Adicionado o CEP que agora é obrigatório)
    sala = Sala(nome="Sala 01", tipo="2D", capacidade=50, cep="70070000")
    db.session.add(sala)
    db.session.commit()

    # Criar evento
    evento = Evento(nome="Show de Rock 2026")
    db.session.add(evento)
    db.session.commit()

    # Criar sessão
    hoje = datetime.now()
    sessao = Sessao(
        horario_data=hoje + timedelta(days=1),
        is_dub=False,
        evento_id=evento.id,
        sala_id=sala.id
    )
    db.session.add(sessao)
    db.session.commit()

    # Criar assentos
    assentos = [Assento(numero=f"A{i}", sala_id=sala.id) for i in range(1, 11)]
    db.session.add_all(assentos)
    db.session.commit()

    # Criar usuário
    usuario = User(name="João Silva", cpf="12345678901")
    db.session.add(usuario)
    db.session.commit()

    return {
        'sala': sala,
        'evento': evento,
        'sessao': sessao,
        'assentos': assentos,
        'usuario': usuario
    }


# ===== TESTES DE EVENTO =====
class TestEvento:

    def test_criar_evento_valido(self, client):
        """Teste: Criar evento com nome válido"""
        response = client.post('/eventos', json={'nome': 'Conferência Tech 2026'})
        assert response.status_code == 201
        assert response.json['evento']['nome'] == 'Conferência Tech 2026'

    def test_criar_evento_sem_nome(self, client):
        """Teste: Validação - Criar evento sem nome deve falhar"""
        response = client.post('/eventos', json={})
        assert response.status_code == 400
        assert 'Dados incompletos' in response.json['error']

    def test_listar_eventos(self, client, setup_data):
        """Teste: Listar todos os eventos"""
        response = client.get('/eventos')
        assert response.status_code == 200
        assert len(response.json) >= 1

    def test_obter_evento_por_id(self, client, setup_data):
        """Teste: Obter evento específico por ID"""
        evento = setup_data['evento']
        response = client.get(f'/eventos/{evento.id}')
        assert response.status_code == 200
        assert response.json['nome'] == evento.nome

    def test_obter_evento_inexistente(self, client):
        """Teste: Obter evento que não existe deve retornar 404"""
        response = client.get('/eventos/999')
        assert response.status_code == 404

    def test_atualizar_evento(self, client, setup_data):
        """Teste: Atualizar nome de evento"""
        evento = setup_data['evento']
        response = client.put(
            f'/eventos/{evento.id}',
            json={'nome': 'Show de Rock Actualizado'}
        )
        assert response.status_code == 200
        assert response.json['evento']['nome'] == 'Show de Rock Actualizado'

    def test_deletar_evento(self, client, setup_data):
        """Teste: Deletar evento e suas sessões associadas"""
        evento = setup_data['evento']
        response = client.delete(f'/eventos/{evento.id}')
        assert response.status_code == 200
        assert 'Evento e sessões deletados com sucesso' in response.json['mensagem']


# ===== TESTES DE USUÁRIO =====
class TestUsuario:

    def test_criar_usuario_valido(self, client):
        """Teste: Criar usuário com CPF válido (11 dígitos)"""
        response = client.post('/users', json={
            'name': 'Maria Santos',
            'cpf': '98765432101'
        })
        assert response.status_code == 201
        assert response.json['usuario']['name'] == 'Maria Santos'

    def test_criar_usuario_com_cpf_sujo(self, client):
        """Teste: Garantir que o backend limpa o CPF formatado antes de salvar"""
        response = client.post('/users', json={
            'name': 'carlos almeida',
            'cpf': '123.456.789-00'
        })
        assert response.status_code == 201
        assert response.json['usuario']['name'] == 'Carlos Almeida'
        assert response.json['usuario']['cpf'] == '12345678900'

    def test_criar_usuario_sem_dados(self, client):
        """Teste: Validação - Criar usuário sem dados deve falhar"""
        response = client.post('/users', json={})
        assert response.status_code == 400
        assert 'Dados incompletos' in response.json['error']

    def test_criar_usuario_cpf_invalido(self, client):
        """Teste: Validação - CPF com menos de 11 dígitos deve falhar"""
        response = client.post('/users', json={
            'name': 'João Silva',
            'cpf': '123'
        })
        assert response.status_code == 400
        assert 'dígitos numéricos' in response.json['error']

    def test_criar_usuario_cpf_duplicado(self, client, setup_data):
        """Teste: Validação - CPF duplicado deve falhar"""
        usuario = setup_data['usuario']
        response = client.post('/users', json={
            'name': 'Outro Usuário',
            'cpf': usuario.cpf  # Mesmo CPF
        })
        assert response.status_code == 400
        assert 'CPF já cadastrado' in response.json['error']

    def test_listar_usuarios(self, client, setup_data):
        """Teste: Listar todos os usuários"""
        response = client.get('/users')
        assert response.status_code == 200
        assert len(response.json) >= 1

    def test_obter_usuario_por_id(self, client, setup_data):
        """Teste: Obter usuário específico"""
        usuario = setup_data['usuario']
        response = client.get(f'/users/{usuario.id}')
        assert response.status_code == 200
        assert response.json['name'] == usuario.name

    def test_atualizar_usuario(self, client, setup_data):
        """Teste: Atualizar nome de usuário"""
        usuario = setup_data['usuario']
        response = client.put(
            f'/users/{usuario.id}',
            json={'name': 'João Silva Atualizado'}
        )
        assert response.status_code == 200
        assert response.json['usuario']['name'] == 'João Silva Atualizado'


# ===== TESTES DE RESERVA =====
class TestReserva:

    def test_criar_reserva_valida(self, client, setup_data):
        """Teste: Caminho feliz - Criar reserva válida"""
        usuario = setup_data['usuario']
        sessao = setup_data['sessao']
        assento = setup_data['assentos'][0]

        response = client.post('/reservas', json={
            'user_id': usuario.id,
            'sessao_id': sessao.id,
            'assento_id': assento.id
        })
        assert response.status_code == 201
        assert response.json['reserva']['user_id'] == usuario.id

    def test_criar_reserva_sem_dados(self, client):
        """Teste: Validação - Criar reserva sem dados deve falhar"""
        response = client.post('/reservas', json={})
        assert response.status_code == 400
        assert 'Dados incompletos' in response.json['error']

    def test_conflito_reserva_mesmo_assento(self, client, setup_data):
        """Teste: CRÍTICO - Impedir reserva duplicada no mesmo assento/sessão"""
        usuario = setup_data['usuario']
        sessao = setup_data['sessao']
        assento = setup_data['assentos'][0]

        # Primeira reserva deve funcionar
        response1 = client.post('/reservas', json={
            'user_id': usuario.id,
            'sessao_id': sessao.id,
            'assento_id': assento.id
        })
        assert response1.status_code == 201

        # Segunda reserva no mesmo assento/sessão deve falhar
        usuario2 = User(name="Pedro Costa", cpf="11122233344")
        db.session.add(usuario2)
        db.session.commit()

        response2 = client.post('/reservas', json={
            'user_id': usuario2.id,
            'sessao_id': sessao.id,
            'assento_id': assento.id
        })
        assert response2.status_code == 400
        assert 'já está reservado' in response2.json['error']

    def test_reserva_usuario_inexistente(self, client, setup_data):
        """Teste: Validação - Reserva com usuário inexistente deve falhar"""
        sessao = setup_data['sessao']
        assento = setup_data['assentos'][0]

        response = client.post('/reservas', json={
            'user_id': 999,  # Usuário inexistente
            'sessao_id': sessao.id,
            'assento_id': assento.id
        })
        assert response.status_code == 400
        assert 'Usuário não encontrado' in response.json['error']

    def test_listar_reservas(self, client, setup_data):
        """Teste: Listar todas as reservas"""
        response = client.get('/reservas')
        assert response.status_code == 200

    def test_deletar_reserva(self, client, setup_data):
        """Teste: Deletar uma reserva existente"""
        usuario = setup_data['usuario']
        sessao = setup_data['sessao']
        assento = setup_data['assentos'][0]

        # Criar reserva
        reserva = Reserva(
            user_id=usuario.id,
            sessao_id=sessao.id,
            assento_id=assento.id
        )
        db.session.add(reserva)
        db.session.commit()

        # Deletar
        response = client.delete(f'/reservas/{reserva.id}')
        assert response.status_code == 200
        assert 'deletada com sucesso' in response.json['mensagem']


# ===== TESTES DE SALA =====
class TestSala:

    def test_criar_sala_valida(self, client):
        """Teste: Criar sala com dados válidos"""
        response = client.post('/salas', json={
            'nome': 'Auditório Principal',
            'tipo': '2D',
            'capacidade': 100,
            'cep': '70790075'
        })
        assert response.status_code == 201
        assert response.json['sala']['nome'] == 'Auditório Principal'

    def test_criar_sala_sem_dados(self, client):
        """Teste: Validação - Criar sala sem dados deve falhar"""
        response = client.post('/salas', json={})
        assert response.status_code == 400

    def test_listar_salas(self, client, setup_data):
        """Teste: Listar todas as salas"""
        response = client.get('/salas')
        assert response.status_code == 200
        assert len(response.json) >= 1


# ===== TESTES DE ASSENTO =====
class TestAssento:

    def test_criar_assento_valido(self, client, setup_data):
        """Teste: Criar assento em sala existente"""
        sala = setup_data['sala']
        response = client.post('/assentos', json={
            'numero': 'A99',
            'sala_id': sala.id
        })
        assert response.status_code == 201
        assert response.json['assento']['numero'] == 'A99'

    def test_listar_assentos(self, client, setup_data):
        """Teste: Listar todos os assentos"""
        response = client.get('/assentos')
        assert response.status_code == 200
        assert len(response.json) >= 1
