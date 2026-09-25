# SaúdeApp 2.0

Projeto acadêmico de simulação de um sistema pessoal de acompanhamento de saúde.

## Novidades da 2.0

- SQLite (`database/saudeapp.db`) no lugar do JSON como armazenamento principal.
- Migração automática inicial a partir de `data/usuarios_backup.json`.
- Históricos e registros separados em tabelas SQLite.
- Validações no servidor para medidas e formulários.
- Agendamentos com validação de data/hora e prevenção de conflito.
- Upload de exames com limite de tamanho e extensões controladas.
- Central de documentos PDF.
- Resumo de saúde, receitas, exames, agendamentos e carteirinha em PDF.
- QR Code de verificação para documentos gerados.
- Todos os PDFs possuem marcação explícita **DOCUMENTO SIMULADO / SEM VALIDADE OFICIAL**.
- Página amigável para erros 404, 413 e 500.
- Navegação ativa, responsiva e visual padronizado.

## Instalação

```bash
python -m venv venv
# Windows
venv\\Scripts\\activate
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000`.

## Banco de dados

O banco é criado automaticamente em `database/saudeapp.db`. Na primeira inicialização, se o banco estiver vazio e `data/usuarios_backup.json` existir, os dados são importados.

O JSON é mantido apenas como backup da migração. Depois da migração, as operações normais usam SQLite.

## Documentos

A área **Documentos** gera PDFs para demonstração da interface de um sistema de saúde. Os documentos são deliberadamente marcados como simulação e não devem ser usados como documentos médicos, receitas, laudos, atestados ou identificações reais.

## Dependências principais

- Flask — aplicação web
- Werkzeug — hash de senha
- SQLite — persistência local
- ReportLab — geração de PDF
- qrcode + Pillow — QR Codes dos documentos

## Banco de dados e foto de perfil

O projeto usa **SQLite** para o banco local. O arquivo fica em `database/saudeapp.db` e é criado automaticamente pelo sistema quando necessário. Ele é um banco `.db` local; não é um servidor MySQL.

O perfil agora permite enviar uma foto em JPG, JPEG, PNG ou WEBP. A imagem fica em `uploads/` e o nome/caminho da foto fica registrado na tabela `usuarios` do `saudeapp.db`.


## Recursos adicionados nesta versão

- Data/hora oficial do servidor em `America/Sao_Paulo`.
- Agendamentos bloqueados no passado, inclusive horário quando a data é hoje.
- Hidratação reiniciada automaticamente quando muda o dia.
- Seletor de idioma: Português, English e Español.
- Preferência de idioma salva por usuário no SQLite.
- Assistente de IA opcional em `/assistente`.
- A IA só é ativada quando `OPENAI_API_KEY` está configurada.

### Ativar o Assistente de IA

No Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="sua-chave-aqui"
$env:OPENAI_MODEL="gpt-5.6-luna"
python app.py
```

Ou instale as dependências:

```bash
pip install -r requirements.txt
```

A IA é apenas um recurso informativo. Ela não diagnostica, prescreve medicamentos nem substitui profissionais de saúde.


## 3.1 — organização e segurança

- Dashboard com tendências, hidratação de 7 dias e gráficos refinados.
- Central de notificações com leitura individual e coletiva.
- Calendário mensal de consultas.
- Configurações com alteração de senha e exportação dos dados em ZIP/JSON/CSV.
- Proteção CSRF em mutações e cookies de sessão endurecidos.
- Uploads com nomes de arquivo seguros.
- Interface redesenhada com linguagem visual inspirada em software corporativo: bordas discretas, tipografia Segoe UI, espaçamento consistente e ausência de gradientes decorativos.

### Produção

Defina `SECRET_KEY` no ambiente e use HTTPS (`FLASK_HTTPS=1`). Deixe `FLASK_DEBUG=0`.
