# Central de Aplicativos | Setta

Hub em Streamlit para acesso centralizado aos aplicativos operacionais.

## Estrutura

- `streamlit_app.py` — aplicação principal.
- `assets/fabrica_setta.png` — imagem do cabeçalho.
- `requirements.txt` — dependências.

## Como adicionar novos aplicativos

Edite a lista `APPS` no início do arquivo `streamlit_app.py`.

Exemplo:

```python
{
    "nome": "Novo Aplicativo",
    "descricao": "Descrição resumida",
    "icone": "⚙️",
    "status": "Online",
    "url": "https://seu-app.streamlit.app",
}
```

O layout gera os cards automaticamente e se adapta para desktop, tablet e celular.

## Executar localmente

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Publicação no Streamlit Community Cloud

- Repositório: selecione este projeto no GitHub.
- Branch: `main`
- Main file path: `streamlit_app.py`
