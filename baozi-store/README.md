# Baozi Store - API REST

API REST simples (Java, Spring Boot, Spring Data JPA) para controle de clientes, produtos e pedidos de uma loja de pao chines.

## Requisitos
- Java 17+
- Maven 3.9+

## Executar (H2 em memoria - padrao)
```bash
mvn spring-boot:run
```
API em `http://localhost:8080`.

## Executar com MySQL
```bash
export DB_HOST=localhost DB_NAME=baozi DB_USER=seu_usuario DB_PASSWORD=sua_senha
export SPRING_PROFILES_ACTIVE=mysql
mvn spring-boot:run
```

## Endpoints
Para `/clientes`, `/produtos` e `/pedidos`:

| Metodo | Rota | Descricao |
|--------|------|-----------|
| POST | /{recurso} | Criar |
| GET | /{recurso} | Listar todos |
| GET | /{recurso}/{id} | Consultar por ID |
| PUT | /{recurso}/{id} | Atualizar (opcional) |
| DELETE | /{recurso}/{id} | Apagar |

## Estrutura
`model` (entidades JPA), `repository` (Spring Data JPA), `controller` (endpoints REST), `exception` (tratamento padronizado de erros).

## Seguranca aplicada
Validacao de entrada (Bean Validation), id nao controlavel pelo chamador, integridade referencial em pedidos, respostas de erro sem vazamento de detalhes internos, credenciais por variavel de ambiente, console H2 desativado.
