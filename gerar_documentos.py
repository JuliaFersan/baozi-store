# -*- coding: utf-8 -*-
"""Gera o PDF da Atividade Pratica e a colecao do Postman.
Edite as variaveis abaixo e rode: python gerar_documentos.py   (requer: pip install reportlab)"""
import json
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
                                KeepTogether)
from reportlab.graphics.shapes import Drawing, Rect, Ellipse, Line, String, Circle

# ===================== EDITE AQUI =====================
NOME = "Julia Sampaio"
RU = "4913744"
CURSO = "ANÁLISE E DESENVOLVIMENTO DE SISTEMAS"
CIDADE_ESTADO = "Braga – Portugal"
ANO = "2026"
PRODUTO = "Baozi de Carne"
PRECO = 4.50
QUANTIDADE = 5
REPO_URL = "https://github.com/SEU_USUARIO/baozi-store"
# ======================================================

CLIENTE_NOME = f"{NOME.replace(' ', '')}{RU}"
HL = "#FFFF00"
def hl(t): return f'<font backColor="{HL}">{t}</font>'

body = ParagraphStyle("body", fontName="Helvetica", fontSize=11, leading=16, alignment=TA_JUSTIFY, spaceAfter=8)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, leading=18, spaceBefore=6, spaceAfter=10)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11.5, leading=15, spaceBefore=8, spaceAfter=6)
cen = ParagraphStyle("cen", parent=body, alignment=TA_CENTER, fontSize=13, leading=20, spaceAfter=2)
cenb = ParagraphStyle("cenb", parent=cen, fontName="Helvetica-Bold")
small = ParagraphStyle("small", fontName="Helvetica", fontSize=9, leading=12)
smallb = ParagraphStyle("smallb", parent=small, fontName="Helvetica-Bold")
code = ParagraphStyle("code", fontName="Courier", fontSize=8.5, leading=11, backColor=colors.HexColor("#F2F2F2"),
                      borderPadding=4, spaceAfter=6)

def P(t, s=body): return Paragraph(t, s)

def tabela(dados, larguras, cab=True):
    t = Table([[Paragraph(str(c), smallb if (cab and i == 0) else small) for c in l] for i, l in enumerate(dados)],
              colWidths=larguras, repeatRows=1 if cab else 0)
    est = [("GRID", (0, 0), (-1, -1), 0.5, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP"),
           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]
    if cab: est.append(("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DDE6F3")))
    t.setStyle(TableStyle(est)); return t

def diagrama():
    W, H = 450, 540
    d = Drawing(W, H)
    # fronteira do sistema
    d.add(Rect(140, 5, 300, 530, strokeColor=colors.black, fillColor=None, strokeWidth=1.2))
    d.add(String(290, 518, "API REST – Baozi Store", fontName="Helvetica-Bold", fontSize=10, textAnchor="middle"))
    # ator
    ax, ay = 40, 280
    d.add(Circle(ax, ay + 55, 9, strokeColor=colors.black, fillColor=None))
    d.add(Line(ax, ay + 46, ax, ay + 12)); d.add(Line(ax - 20, ay + 36, ax + 20, ay + 36))
    d.add(Line(ax, ay + 12, ax - 16, ay - 12)); d.add(Line(ax, ay + 12, ax + 16, ay - 12))
    d.add(String(ax, ay - 28, "Usuário da API", fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))
    casos = []
    for ent, art in (("cliente", "o"), ("produto", "o"), ("pedido", "o")):
        casos += [f"Cadastrar {ent}", f"Listar todos os {ent}s", f"Consultar {ent} por ID",
                  f"Atualizar {ent}", f"Apagar {ent}"]
    top, passo = 485, 31
    for i, c in enumerate(casos):
        cy = top - i * passo
        d.add(Line(ax + 8, ay + 30, 190, cy, strokeColor=colors.HexColor("#555555"), strokeWidth=0.6))
        d.add(Ellipse(290, cy, 100, 12, strokeColor=colors.black, fillColor=colors.HexColor("#EAF1FB")))
        d.add(String(290, cy - 3, c, fontName="Helvetica", fontSize=8, textAnchor="middle"))
    return d

def retangulo_print(titulo, req, exemplo):
    caixa = Table([[Paragraph(hl("[INSERIR AQUI O PRINT DO POSTMAN]"), small)]], colWidths=[16 * cm], rowHeights=[3.2 * cm])
    caixa.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.8, colors.grey), ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                               ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return KeepTogether([P(titulo, h2), P(req, small), P(exemplo, code), caixa, Spacer(1, 6)])

def rodape(c, doc):
    if doc.page > 1:
        c.setFont("Helvetica", 8); c.setFillColor(colors.grey)
        c.drawCentredString(A4[0] / 2, 1.2 * cm, f"Desenvolvimento Web Back End – Atividade Prática – {doc.page}")

story = []
# ---- Capa ----
story += [Spacer(1, 3.5 * cm), P("CENTRO UNIVERSITÁRIO INTERNACIONAL UNINTER", cen), P("ESCOLA SUPERIOR POLITÉCNICA", cen),
          P(hl(CURSO), cen), P("DESENVOLVIMENTO WEB BACK END", cen), Spacer(1, 4 * cm),
          P("ATIVIDADE PRÁTICA", cenb), P("API REST – BAOZI STORE", cenb), Spacer(1, 4.5 * cm),
          P(hl(f"{NOME.upper()} – RU: {RU}"), ParagraphStyle("r", parent=cen, alignment=2, fontSize=11)),
          Spacer(1, 3.2 * cm), P(hl(CIDADE_ESTADO), cen), P(ANO, cen), PageBreak()]

# ---- 1 ----
story += [P("ATIVIDADE PRÁTICA", h1), P("1. Descrição de uma situação fictícia", h1),
          P(f"A <b>Baozi Store</b> é uma pequena loja que vende <b>pão chinês</b>. Para melhorar a organização do negócio, "
            f"foi criado um sistema simples para controlar clientes, produtos e pedidos."),
          P(f"Um cliente chamado <b>{hl(CLIENTE_NOME)}</b> realizou seu cadastro no sistema. O produto vendido pela loja "
            f"chama-se <b>{PRODUTO}</b> e é vendido por unidade, ao preço de {PRECO:.2f}. Em um determinado momento, o cliente "
            f"realizou um pedido de <b>{QUANTIDADE}</b> unidades do produto."),
          P("O sistema registra o cliente, o produto comprado e a quantidade solicitada, facilitando o controle da loja."),
          P("<b>Dados utilizados nos testes (presentes nos prints do Postman):</b>"),
          tabela([["Entidade", "Dados"],
                  ["Cliente", f"nome: {CLIENTE_NOME}"],
                  ["Produto", f"nome: {PRODUTO}; preco: {PRECO:.2f}; estoque: true"],
                  ["Pedido", f"cliente: {CLIENTE_NOME} (id 1); produto: {PRODUTO} (id 1); quantidade: {QUANTIDADE}"]],
                 [3 * cm, 13 * cm]), PageBreak()]

# ---- 2 ----
story += [P("2. Diagrama caso de uso", h1),
          P("Diagrama de Caso de Uso UML com o ator principal (Usuário da API) e os casos de uso do CRUD de Cliente, "
            "Produto e Pedido implementados na API REST.", body), diagrama(), PageBreak()]

# ---- 3 ----
story += [P("3. Especificação da API desenvolvida", h1),
          P("Tecnologias: Java 17, Spring Boot, Spring Data JPA, banco relacional H2 (perfil alternativo MySQL), JSON nos "
            "endpoints, padrão MVC do Spring. Pacotes: <i>model</i>, <i>repository</i>, <i>controller</i> (e <i>exception</i> "
            "para tratamento de erros)."),
          P("3.1 Entidades criadas e campos", h2),
          tabela([["Entidade", "Campo", "Tipo", "Regras"],
                  ["Cliente", "id", "Long", "Chave primária, gerada automaticamente"],
                  ["", "nome", "String", "Obrigatório, até 100 caracteres"],
                  ["", "clienteDesde", "LocalDate", "Não pode ser data futura; padrão: data atual"],
                  ["Produto", "id", "Long", "Chave primária, gerada automaticamente"],
                  ["", "nome", "String", "Obrigatório, até 100 caracteres"],
                  ["", "preco", "BigDecimal", "Obrigatório, maior que zero, 2 casas decimais"],
                  ["", "estoque", "Boolean", "Obrigatório (true = disponível)"],
                  ["Pedido", "id", "Long", "Chave primária, gerada automaticamente"],
                  ["", "clienteId", "Long", "Obrigatório; deve referenciar cliente existente"],
                  ["", "produtoId", "Long", "Obrigatório; deve referenciar produto existente com estoque"],
                  ["", "quantidade", "Integer", "Obrigatório, entre 1 e 1000"]],
                 [2.4 * cm, 3 * cm, 2.8 * cm, 7.8 * cm]),
          P("3.2 Endpoints implementados", h2)]
ends = [["Método", "Rota", "Descrição", "Resposta"]]
for r, n in (("clientes", "cliente"), ("produtos", "produto"), ("pedidos", "pedido")):
    ends += [["POST", f"/{r}", f"Criar {n}", "201 Created"],
             ["GET", f"/{r}", f"Listar todos", "200 OK"],
             ["GET", f"/{r}/{{id}}", f"Consultar por ID", "200 OK / 404"],
             ["PUT", f"/{r}/{{id}}", "Atualizar (opcional)", "200 OK / 404"],
             ["DELETE", f"/{r}/{{id}}", "Apagar", "204 No Content / 404 / 409"]]
story += [tabela(ends, [2.2 * cm, 3.6 * cm, 5.6 * cm, 4.6 * cm]),
          P("3.3 Boas práticas de segurança aplicadas", h2),
          tabela([["Controle", "Implementação"],
                  ["Validação de entrada", "Bean Validation (@Valid, @NotBlank, @Positive, @Min/@Max) com resposta 400 e mensagens por campo"],
                  ["Mass assignment", "O id é sempre ignorado no POST; o banco o gera"],
                  ["Integridade referencial", "Pedido só é aceito com cliente e produto existentes e produto em estoque; "
                                              "cliente/produto com pedidos não podem ser apagados (409)"],
                  ["Tratamento de erros", "Handler global devolve mensagens genéricas; stack trace, SQL e nomes de classes ficam apenas no log do servidor"],
                  ["Gestão de credenciais", "Banco MySQL configurado por variáveis de ambiente; nenhuma senha no repositório"],
                  ["Redução de superfície", "Console H2 desativado; JSON como único formato de troca"]],
                 [4 * cm, 12 * cm]), PageBreak()]

# ---- 4 ----
cj = json.dumps({"nome": CLIENTE_NOME}, ensure_ascii=False)
pj = json.dumps({"nome": PRODUTO, "preco": PRECO, "estoque": True}, ensure_ascii=False)
oj = json.dumps({"clienteId": 1, "produtoId": 1, "quantidade": QUANTIDADE}, ensure_ascii=False)
story += [P("4. Prints do Postman", h1),
          P("Prints obrigatórios, cada um com as informações da descrição (cliente, produto e quantidade) visíveis.")]
story += [retangulo_print("4.1 POST /clientes", "Body (raw, JSON):", cj),
          retangulo_print("4.2 POST /produtos", "Body (raw, JSON):", pj),
          retangulo_print("4.3 POST /pedidos", "Body (raw, JSON):", oj),
          retangulo_print("4.4 GET geral", "GET /clientes, GET /produtos e GET /pedidos (um print para cada, ou um por rota).", "GET http://localhost:8080/clientes"),
          retangulo_print("4.5 GET por ID", "GET /pedidos/1 (e, se desejar, /clientes/1 e /produtos/1).", "GET http://localhost:8080/pedidos/1"),
          retangulo_print("4.6 DELETE", "DELETE /pedidos/1 retorna 204. Em seguida, GET /pedidos/1 retorna 404.", "DELETE http://localhost:8080/pedidos/1"),
          PageBreak()]

# ---- 5 ----
story += [P("5. Link do repositório (GitHub ou similar) contendo o projeto (código fonte)", h1),
          P(hl(REPO_URL))]

SimpleDocTemplate("Atividade_Pratica_Baozi_Store.pdf", pagesize=A4, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
                  topMargin=2.2 * cm, bottomMargin=2.2 * cm, title="Atividade Prática – Baozi Store",
                  author=NOME).build(story, onFirstPage=rodape, onLaterPages=rodape)

# ---- Colecao Postman ----
def req(nome, metodo, caminho, corpo=None):
    r = {"method": metodo, "header": [], "url": {"raw": "{{baseUrl}}" + caminho, "host": ["{{baseUrl}}"],
                                                 "path": [p for p in caminho.split("/") if p]}}
    if corpo is not None:
        r["header"] = [{"key": "Content-Type", "value": "application/json"}]
        r["body"] = {"mode": "raw", "raw": json.dumps(corpo, ensure_ascii=False, indent=2),
                     "options": {"raw": {"language": "json"}}}
    return {"name": nome, "request": r}
col = {"info": {"name": "Baozi Store", "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},
       "variable": [{"key": "baseUrl", "value": "http://localhost:8080"}],
       "item": [req("1. POST Cliente", "POST", "/clientes", {"nome": CLIENTE_NOME}),
                req("2. POST Produto", "POST", "/produtos", {"nome": PRODUTO, "preco": PRECO, "estoque": True}),
                req("3. POST Pedido", "POST", "/pedidos", {"clienteId": 1, "produtoId": 1, "quantidade": QUANTIDADE}),
                req("4. GET Clientes", "GET", "/clientes"), req("5. GET Produtos", "GET", "/produtos"),
                req("6. GET Pedidos", "GET", "/pedidos"), req("7. GET Cliente por ID", "GET", "/clientes/1"),
                req("8. GET Produto por ID", "GET", "/produtos/1"), req("9. GET Pedido por ID", "GET", "/pedidos/1"),
                req("10. DELETE Pedido", "DELETE", "/pedidos/1"),
                req("11. GET Pedido apagado (404)", "GET", "/pedidos/1")]}
json.dump(col, open("baozi-store.postman_collection.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("OK")
