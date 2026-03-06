# AI RPG Agent (D&D 5e)

Um agente de AI que **gera e aconselha personagens de D&D 5ª edição**, seguindo **as regras do Player’s Handbook (PHB)**.

Para esse desafio foi escolhido a OpenAI pra ter um controle maior sobre a lógica do modelo, sobre a separação do generator com o advisor e também no controle de regras do D&D

---
## 🎬 Demonstração 

https://youtu.be/K0OMV2vjZts
---
## ✨ Funcionalidades

*  **Geração de Personagens (PHB apenas)**

  * Personagens de nível 1-3
  * Atributos por Point Buy
  * Classes, raças e backgrounds do PHB
  * Equipamentos, proficiências, magias e habilidades gerados automaticamente

*  **Modo Advisor (Somente leitura)**

  * Explica mecânicas
  * Dá dicas de gameplay e roleplay

*  **Validação Local de Regras**

  * Personagens são validados localmente após a geração
  * Garante conformidade com as regras do PHB

---

## 🧠 Arquitetura

O sistema é dividido intencionalmente em **três componentes principais**:

---

###  Pipeline de Geração

Responsável por **criar um novo personagem** a partir de um pedido em linguagem natural.

Funções:

* Interpretar a intenção do usuário 
* Gerar uma ficha completa de personagem
* Executar validação local

Este pipeline **só é executado** quando:

* A aplicação é iniciada
* O usuário solicita explicitamente um novo personagem

---

### Advisor

* Responde perguntas sobre o personagem atual
* Explica regras e mecânicas
* Recusa alterações que quebram as regras


###  Regras

Conjunto regras carregadas a partir do arquivo JSON (phb_min_rules), podendo ser expandido no futuro.

* Classes, raças e backgrounds permitidos
* Restrições de atributos (Point Buy)
* Regras de proficiências
* Regras de conjuração

Isso permite:

* Validação determinística
* Redução de alucinações do LLM
* Aplicação das regras

---

## ⚙️ Tecnologias Utilizadas

* **Python 3.14**
* **OpenAI API** (LLM)
* **JSON** para definição de regras

---

## 🔐 Variáveis de Ambiente


### `.env.template` (versionado)

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o-mini
```

---

## ▶️ Como Executar

```bash
python app.py
```

Siga as instruções no terminal para gerar e interagir com seu personagem.

---

## 📌 Comandos Importantes

* `new character` → descarta o personagem atual e inicia uma nova geração
* `exit` → encerra a aplicação
