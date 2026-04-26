import os
import sys
import subprocess
import platform
import time

# Códigos de cor para um terminal bonito
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

MODELO_REQUERIDO = "qwen2.5-coder:7b"

def print_step(texto):
    print(f"{Colors.OKBLUE}[*]{Colors.ENDC} {texto}")

def print_success(texto):
    print(f"{Colors.OKGREEN}[✓]{Colors.ENDC} {texto}")

def print_error(texto):
    print(f"{Colors.FAIL}[x]{Colors.ENDC} {texto}")

def check_command(command):
    """Verifica se um comando existe no sistema (ex: ollama, npm)"""
    try:
        subprocess.run([command, '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except FileNotFoundError:
        return False
    except subprocess.CalledProcessError:
        return True # O comando existe, mas --version deu erro (incomum, mas possível)

def install_ollama_linux():
    print_step("Iniciando instalação automatizada do Ollama para Linux...")
    try:
        # Roda o script oficial de instalação do Ollama
        subprocess.run("curl -fsSL https://ollama.com/install.sh | sh", shell=True, check=True)
        print_success("Ollama instalado com sucesso!")
    except subprocess.CalledProcessError:
        print_error("Falha ao instalar o Ollama. Execute manualmente: curl -fsSL https://ollama.com/install.sh | sh")
        sys.exit(1)

def setup_ollama():
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== 🏺 SETUP DO AMBIENTE ARQUEÓLOGO ==={Colors.ENDC}\n")
    
    # 1. Verifica se o Ollama está instalado
    print_step("Verificando instalação do motor de IA (Ollama)...")
    time.sleep(1)
    
    if check_command('ollama'):
        print_success("Ollama detectado no sistema.")
    else:
        print_error("Ollama não encontrado.")
        sistema = platform.system()
        
        if sistema == "Linux":
            resposta = input(f"{Colors.WARNING}Deseja instalar o Ollama agora? (s/n): {Colors.ENDC}").strip().lower()
            if resposta == 's':
                install_ollama_linux()
            else:
                print_error("A instalação foi cancelada. O Arqueólogo precisa do Ollama para funcionar.")
                sys.exit(1)
        elif sistema == "Windows":
            print_step("No Windows, a instalação precisa ser manual.")
            print(f"{Colors.OKCYAN}👉 Baixe e instale aqui: https://ollama.com/download/windows{Colors.ENDC}")
            print("Após instalar, feche este terminal, abra um novo e rode este script novamente.")
            sys.exit(1)
        else:
            print_error(f"Sistema {sistema} não suportado pelo instalador automático. Baixe em ollama.com")
            sys.exit(1)

    # 2. Verifica/Baixa o Modelo
    print_step(f"Verificando se o modelo '{MODELO_REQUERIDO}' está presente...")
    try:
        resultado = subprocess.run(['ollama', 'list'], stdout=subprocess.PIPE, text=True, check=True)
        if MODELO_REQUERIDO in resultado.stdout:
            print_success(f"Modelo {MODELO_REQUERIDO} já está instalado e pronto para uso!")
        else:
            print_step(f"Modelo {MODELO_REQUERIDO} não encontrado. Isso pode demorar alguns minutos dependendo da sua internet...")
            # Deixa a saída ir para a tela para o usuário ver a barra de progresso do Ollama
            subprocess.run(['ollama', 'pull', MODELO_REQUERIDO], check=True)
            print_success(f"Modelo baixado com sucesso!")
    except subprocess.CalledProcessError:
        print_error("O serviço do Ollama não está rodando. Digite 'ollama serve' em outro terminal e tente novamente.")
        sys.exit(1)

    # 3. Empacotando a extensão (Opcional, mas útil)
    print_step("Verificando se a extensão precisa ser compilada...")
    if check_command('npm'):
        if not os.path.exists('node_modules'):
            print_step("Instalando dependências do Node...")
            subprocess.run(['npm', 'install'], check=True)
        print_success("Ambiente de desenvolvimento VS Code validado.")
    
    print(f"\n{Colors.OKGREEN}{Colors.BOLD}🎉 TUDO PRONTO! O Arqueólogo está com o motor ligado e pronto para escavar.{Colors.ENDC}\n")

if __name__ == "__main__":
    setup_ollama()