import os
from app import app
from services import UserService, EventoService, SessaoService, AssentoService, SalaService, ReservaService
def menu():
    print("\n--- 🎬 CineComunidade: Menu de Gestão ---")
    print("1. Listar Sessões Disponíveis")
    print("2. Fazer uma Reserva")
    print("3. Sair")
    return input("Escolha uma opção: ")

def rodar_cli():
    with app.app_context():
        while True:
            opcao = menu()
            if opcao == "1":

                print("\nListando sessões...") 
            elif opcao == "2":
                u_id = input("ID do Usuário: ")
                s_id = input("ID da Sessão: ")
                a_id = input("ID do Assento: ")
                try:
                    reserva = ReservaService.criar_reserva(u_id, s_id, a_id)
                    print(f"✅ Sucesso! Reserva ID {reserva.id} confirmada.")
                except Exception as e:
                    print(f"❌ Erro: {e}")
            elif opcao == "3":
                break

if __name__ == "__main__":
    rodar_cli()