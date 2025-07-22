from datetime import datetime
from typing import List, Tuple
import logging

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ContaBancaria:
    """Classe para representar uma conta bancária com suas operações."""

    def __init__(self, limite_saque: float = 500.0, limite_saques_diarios: int = 3, taxa_servico: float = 0.015):
        self.saldo = 0.0
        self.extrato: List[dict] = []
        self.limite_saque = limite_saque
        self.limite_saques_diarios = limite_saques_diarios
        self.taxa_servico = taxa_servico
        self.numero_saques_hoje = 0
        self.data_ultimo_saque = None

    def _registrar_movimento(self, tipo: str, valor: float, taxa: float = 0.0) -> None:
        """Registra um movimento no extrato com timestamp."""
        movimento = {
            'tipo': tipo,
            'valor': valor,
            'taxa': taxa,
            'timestamp': datetime.now(),
            'saldo_resultante': self.saldo
        }
        self.extrato.append(movimento)
        logging.info(f"{tipo} de R$ {valor:.2f} realizado. Saldo atual: R$ {self.saldo:.2f}")

    def _verificar_limite_saques_diarios(self) -> bool:
        """Verifica se ainda é possível realizar saques hoje."""
        hoje = datetime.now().date()

        # Reset contador se mudou o dia
        if self.data_ultimo_saque != hoje:
            self.numero_saques_hoje = 0

        return self.numero_saques_hoje < self.limite_saques_diarios

    def depositar(self, valor: float) -> bool:
        """
        Realiza um depósito na conta.

        Args:
            valor (float): Valor a ser depositado

        Returns:
            bool: True se o depósito foi realizado com sucesso
        """
        try:
            valor = float(valor)
            if valor <= 0:
                print("❌ Operação falhou! O valor deve ser positivo.")
                return False

            self.saldo += valor
            self._registrar_movimento("Depósito", valor)
            print(f"✅ Depósito de R$ {valor:.2f} realizado com sucesso!")
            return True

        except (ValueError, TypeError):
            print("❌ Operação falhou! Valor inválido.")
            return False

    def sacar(self, valor: float) -> bool:
        """
        Realiza um saque da conta.

        Args:
            valor (float): Valor a ser sacado

        Returns:
            bool: True se o saque foi realizado com sucesso
        """
        try:
            valor = float(valor)
            if valor <= 0:
                print("❌ Operação falhou! O valor deve ser positivo.")
                return False

            # Verificar limite de saques diários
            if not self._verificar_limite_saques_diarios():
                print(f"❌ Operação falhou! Limite de {self.limite_saques_diarios} saques diários excedido.")
                return False

            # Verificar limite por saque
            if valor > self.limite_saque:
                print(f"❌ Operação falhou! Valor excede o limite de R$ {self.limite_saque:.2f} por saque.")
                return False

            # Calcular taxa de serviço
            taxa_servico = valor * self.taxa_servico
            valor_total = valor + taxa_servico

            # Verificar saldo suficiente
            if valor_total > self.saldo:
                print(f"❌ Operação falhou! Saldo insuficiente. Necessário: R$ {valor_total:.2f} (incluindo taxa).")
                return False

            # Realizar o saque
            self.saldo -= valor_total
            self.numero_saques_hoje += 1
            self.data_ultimo_saque = datetime.now().date()

            self._registrar_movimento("Saque", valor, taxa_servico)
            print(f"✅ Saque de R$ {valor:.2f} realizado com sucesso!")
            print(f"💰 Taxa de serviço: R$ {taxa_servico:.2f}")
            return True

        except (ValueError, TypeError):
            print("❌ Operação falhou! Valor inválido.")
            return False

    def exibir_extrato(self) -> None:
        """Exibe o extrato detalhado da conta."""
        print("\n" + "="*50)
        print("🏦 EXTRATO BANCÁRIO".center(50))
        print("="*50)

        if not self.extrato:
            print("📝 Nenhuma movimentação encontrada.")
        else:
            print(f"{'Data/Hora':<20} {'Tipo':<10} {'Valor':<12} {'Taxa':<10} {'Saldo':<12}")
            print("-"*50)

            for movimento in self.extrato:
                timestamp = movimento['timestamp'].strftime("%d/%m/%Y %H:%M")
                tipo = movimento['tipo']
                valor = f"R$ {movimento['valor']:.2f}"
                taxa = f"R$ {movimento['taxa']:.2f}" if movimento['taxa'] > 0 else "-"
                saldo = f"R$ {movimento['saldo_resultante']:.2f}"

                print(f"{timestamp:<20} {tipo:<10} {valor:<12} {taxa:<10} {saldo:<12}")

        print("-"*50)
        print(f"💳 Saldo atual: R$ {self.saldo:.2f}")
        print(f"📊 Saques restantes hoje: {self.limite_saques_diarios - self.numero_saques_hoje}")
        print("="*50 + "\n")

    def obter_informacoes_conta(self) -> dict:
        """Retorna informações resumidas da conta."""
        return {
            'saldo': self.saldo,
            'limite_saque': self.limite_saque,
            'saques_restantes': self.limite_saques_diarios - self.numero_saques_hoje,
            'total_movimentacoes': len(self.extrato)
        }


class SistemaBancario:
    """Classe principal para gerenciar o sistema bancário."""

    def __init__(self):
        self.conta = ContaBancaria()
        self.executando = True

    def exibir_menu(self) -> str:
        """Exibe o menu principal e retorna a opção escolhida."""
        print("\n🏦 SISTEMA BANCÁRIO")
        print("="*30)
        print("🔹 [d] Depositar")
        print("🔹 [s] Sacar")
        print("🔹 [e] Extrato")
        print("🔹 [i] Informações da conta")
        print("🔹 [q] Sair")
        print("="*30)

        return input("👉 Escolha uma opção: ").strip().lower()

    def processar_deposito(self) -> None:
        """Processa a operação de depósito."""
        try:
            valor_str = input("💰 Informe o valor do depósito: R$ ")
            valor = float(valor_str.replace(',', '.'))
            self.conta.depositar(valor)
        except ValueError:
            print("❌ Valor inválido! Use apenas números.")

    def processar_saque(self) -> None:
        """Processa a operação de saque."""
        try:
            valor_str = input("💸 Informe o valor do saque: R$ ")
            valor = float(valor_str.replace(',', '.'))
            self.conta.sacar(valor)
        except ValueError:
            print("❌ Valor inválido! Use apenas números.")

    def exibir_informacoes(self) -> None:
        """Exibe informações resumidas da conta."""
        info = self.conta.obter_informacoes_conta()
        print(f"\n📊 INFORMAÇÕES DA CONTA")
        print(f"💳 Saldo atual: R$ {info['saldo']:.2f}")
        print(f"🔒 Limite por saque: R$ {info['limite_saque']:.2f}")
        print(f"📈 Saques restantes hoje: {info['saques_restantes']}")
        print(f"📋 Total de movimentações: {info['total_movimentacoes']}")

    def executar(self) -> None:
        """Loop principal do sistema."""
        print("🎉 Bem-vindo ao Sistema Bancário!")

        while self.executando:
            try:
                opcao = self.exibir_menu()

                match opcao:
                    case "d":
                        self.processar_deposito()
                    case "s":
                        self.processar_saque()
                    case "e":
                        self.conta.exibir_extrato()
                    case "i":
                        self.exibir_informacoes()
                    case "q":
                        print("👋 Obrigado por usar nosso sistema bancário!")
                        self.executando = False
                    case _:
                        print("❌ Opção inválida! Tente novamente.")

            except KeyboardInterrupt:
                print("\n\n👋 Sistema encerrado pelo usuário.")
                self.executando = False
            except Exception as e:
                logging.error(f"Erro inesperado: {e}")
                print("❌ Ocorreu um erro inesperado. Tente novamente.")


def main():
    """Função principal para executar o sistema."""
    sistema = SistemaBancario()
    sistema.executar()


if __name__ == "__main__":
    main()
