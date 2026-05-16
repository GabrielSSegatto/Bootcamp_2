from app import app
from models import db, User, Evento, Sessao, Assento, Sala, Reserva
from datetime import datetime, timedelta

def popular_banco():
    with app.app_context():
        if User.query.first():
            print("⚠️ O banco já possui dados! Limpe o banco antes de rodar o seed novamente.")
            return

        print("Enchendo o tanque do banco de dados...")

        sala1 = Sala(nome="Auditório Norte", tipo="IMAX", capacidade=10, cep="70790075")
        sala2 = Sala(nome="Espaço Cultural", tipo="3D", capacidade=10, cep="70070000")
        db.session.add_all([sala1, sala2])
        db.session.commit()

        print("Instalando os assentos...")
        assentos = []
        for i in range(1, 11):
            assentos.append(Assento(numero=f"A{i}", sala_id=sala1.id))
            assentos.append(Assento(numero=f"B{i}", sala_id=sala2.id))
        db.session.add_all(assentos)

        evento1 = Evento(nome="Workshop de Tecnologia")
        evento2 = Evento(nome="Cine Debate Comunitário")
        db.session.add_all([evento1, evento2])
        db.session.commit()

        hoje = datetime.now()
        sessao1 = Sessao(
            horario_data=hoje + timedelta(days=1, hours=2), 
            is_dub=False, 
            evento_id=evento1.id, 
            sala_id=sala1.id
        )
        sessao2 = Sessao(
            horario_data=hoje + timedelta(days=2, hours=5), 
            is_dub=True, 
            evento_id=evento2.id, 
            sala_id=sala2.id
        )
        db.session.add_all([sessao1, sessao2])
        db.session.commit()

        user1 = User(name="João Gabriel", cpf="12345678901")
        user2 = User(name="Gabriel Soares", cpf="10987654321")
        db.session.add_all([user1, user2])
        db.session.commit()

        primeiro_assento = Assento.query.filter_by(sala_id=sala1.id).first()
        reserva1 = Reserva(user_id=user1.id, sessao_id=sessao1.id, assento_id=primeiro_assento.id)
        db.session.add(reserva1)
        db.session.commit()

        print("✅ Banco populado com sucesso!")

if __name__ == '__main__':
    popular_banco()