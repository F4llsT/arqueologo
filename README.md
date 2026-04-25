# 🏺 Arqueólogo de Código (Local AI)

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Ollama](https://img.shields.io/badge/AI-Ollama_Local-orange.svg)
![Privacy](https://img.shields.io/badge/Privacy-100%25_Offline-success.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

O **Arqueólogo** é uma ferramenta de linha de comando (CLI) focada em **Engenharia Reversa, Análise e Documentação Automática** de sistemas legados. 

Construído para ambientes corporativos de alta segurança (Air-gapped), ele utiliza Modelos de Linguagem Locais (LLMs) para analisar códigos confusos e gerar documentação técnica estruturada **sem que nenhuma linha de código proprietário vaze para a internet**.

---

## 🎯 O Problema (Por que usar?)

Bancos, seguradoras e grandes corporações lidam diariamente com bases de código antigas e sem documentação. No entanto, desenvolvedores são frequentemente proibidos de colar essas funções em IAs na nuvem (como ChatGPT ou Claude) devido a rigorosas **políticas de segurança, NDAs e leis de privacidade (LGPD/GDPR)**.

## 💡 A Solução

O Arqueólogo resolve esse gargalo processando múltiplos arquivos 100% offline. Ele atua como um revisor sênior que:
1. Varre diretórios de código legado.
2. Isola as funções e envia para um modelo de IA rodando na própria máquina do desenvolvedor.
3. Gera relatórios individuais apontando propósito, parâmetros, *code smells* e sugestões de refatoração para *Clean Code*.

---

## ⚙️ Funcionalidades Principais

* **🔒 Zero-Data-Leak:** Integração exclusiva com a API local do Ollama. Seus dados nunca saem do seu hardware.
* **📦 Zero Dependências:** Escrito em Python puro utilizando apenas bibliotecas nativas (`os`, `sys`, `json`, `urllib`). Não requer ambientes virtuais complexos ou `pip install`.
* **🤖 Prompt Engineering Embutido:** A ferramenta já encapsula um prompt mestre testado e validado, garantindo que a saída da IA seja sempre padronizada e profissional.
* **🔄 Processamento em Lote (Batch):** Capacidade de percorrer pastas de forma recursiva, isolando erros de arquivos individuais para não interromper a esteira de análise.

---

## 🚀 Como Começar (Quickstart)

### Pré-requisitos
* Python 3.x instalado.
* [Ollama](https://ollama.com/) instalado e rodando em segundo plano.

### Instalação e Execução

1. **Baixe o modelo de IA recomendado (Otimizado para código):**
   ```bash
   ollama pull qwen2.5-coder:7b