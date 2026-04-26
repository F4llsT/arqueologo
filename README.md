# 🏺 Arqueólogo (Local AI - v1.1.0)

O **Arqueólogo** é uma ferramenta de **Engenharia Reversa, Auditoria de Segurança e Documentação Automática** para sistemas legados. Utiliza Modelos de Linguagem Locais (LLMs) para analisar códigos complexos e gerar relatórios técnicos **100% offline**, garantindo que nenhum dado sensível saia da sua infraestrutura.

---

## 🎯 O Problema
Empresas lidam com códigos legados obscuros e sem documentação. O uso de IAs na nuvem é frequentemente bloqueado por políticas de segurança e leis de privacidade (**LGPD/GDPR**). O Arqueólogo traz a inteligência para dentro da máquina do desenvolvedor, eliminando o risco de vazamento de dados.

## 💡 A Solução: Versão 1.1.0
Mais do que uma simples documentação, a versão atual atua como um **Especialista em Segurança (AppSec)** e um **Arquiteto de Software**, entregando:
1. **Auditoria SAST:** Identificação de vulnerabilidades (Hardcoded Secrets, SQL Injections, falhas OWASP).
2. **Análise Cirúrgica:** Análise instantânea de trechos selecionados para respostas rápidas.
3. **Suporte Poliglota:** Entendimento de múltiplas linguagens (JS, TS, Python, Java, PHP, C#, Go, etc).

---

## ⚙️ Funcionalidades Principais
* **🔒 Local First:** Integração via API local do Ollama. Privacidade total.
* **🛡️ Auditoria de Segurança:** Seção dedicada a apontar riscos críticos, médios e baixos.
* **🖱️ Análise por Seleção:** Clique com o botão direito em um trecho de código e receba a análise na hora.
* **📂 Processamento em Lote:** Varredura recursiva de pastas inteiras.
* **⚡ Cache Inteligente:** Utiliza hashes MD5 para evitar reprocessamento de arquivos inalterados.

---

## 🚀 Instalação e Setup Automatizado

### Pré-requisitos
* Python 3.x e Node.js instalados.

### Passo a Passo
1. **Clone o repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/arqueologo.git
   cd arqueologo
   ```

2. **Rode o Setup Automatizado:**
   Este comando verifica o sistema, instala o Ollama (Linux) e baixa o modelo `qwen2.5-coder:7b` automaticamente.
   ```bash
   npm run setup
   ```

---

## 🖱️ Como Usar no VS Code

### 1. Documentação de Arquivo ou Pasta
Na barra lateral (Explorer), clique com o botão direito em um arquivo ou pasta e selecione:
> **🏺 Arqueólogo: Analisar Arquivo/Pasta**
> *O relatório será salvo em `documentacao_gerada/`.*

### 2. Análise de Trecho Específico
Selecione um bloco de código no editor, clique com o botão direito e escolha:
> **🏺 Arqueólogo: Analisar Seleção**
> *Um relatório temporário abrirá ao lado para consulta imediata sem poluir o projeto.*

---

## 📊 Estrutura do Relatório Gerado
* **Propósito Geral:** Explicação em linguagem humana.
* **Clean Code:** Identificação de problemas de lógica e "code smells".
* **Auditoria de Segurança (SAST):** Riscos de vulnerabilidades e possíveis impactos baseados na OWASP.
* **Sugestão de Refatoração:** Código moderno, tipado e seguro.

---

## 🛠️ Tecnologias
* **Motor de IA:** [Ollama](https://ollama.com/) local.
* **Modelo Sugerido:** `qwen2.5-coder:7b`.
* **Backend:** Python 3 (Bibliotecas nativas).
* **Frontend:** VS Code Extension API (TypeScript).

---

## 📄 Licença
Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

---
**Desenvolvido para desenterrar o futuro em códigos do passado.**