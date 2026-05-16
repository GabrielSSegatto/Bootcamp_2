import os
from app import app
from services import UserService, EventoService, SessaoService, AssentoService, SalaService, ReservaService, CEPService

def menu():
    print("\n--- 🎬 CineComunidade: Menu de Gestão ---")
    print("1. Listar Sessões e Localização")
    print("2. Fazer uma Reserva")
    print("3. Sair")
    return input("Escolha uma opção: ")

def rodar_cli():
    with app.app_context():
        while True:
            opcao = menu()
            if opcao == "1":
                print("\n--- 📅 Sessões Disponíveis ---")
                sessoes = SessaoService.get_all_sessoes() 
                
                if not sessoes:
                    print("Nenhuma sessão cadastrada.")
                else:
                    for s in sessoes:
                        # Usando o seu CEPService para buscar os dados
                        dados_cep = CEPService.buscar_endereco(s.sala.cep)
                        
                        if dados_cep:
                            local = f"{dados_cep['logradouro']}, {dados_cep['localidade']}/{dados_cep['uf']}"
                        else:
                            local = f"CEP {s.sala.cep} (Endereço não encontrado)"

                        print(f"\n🎥 Evento: {s.evento.nome}")
                        print(f"⏰ Horário: {s.horario_data}")
                        print(f"🏛️  Sala: {s.sala.nome}")
                        print(f"📍 Local: {local}")
                        print("-" * 30)

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