# README — Olist Orders Dataset

## Sobre a base

O arquivo `olist_orders_dataset.csv` contém informações sobre os pedidos realizados na plataforma de e-commerce da Olist.

Cada linha da base representa **um pedido realizado**.

A tabela possui as seguintes colunas:

| Coluna                          | Descrição                                                    |
|---------------------------------|--------------------------------------------------------------|
| `order_id`                      | Identificador único do pedido                                |
| `customer_id`                   | Identificador do cliente associado ao pedido                 |
| `order_status`                  | Situação do pedido                                           |
| `order_purchase_timestamp`      | Data e horário em que a compra foi realizada                 |
| `order_approved_at`             | Data e horário em que o pedido foi aprovado                  |
| `order_delivered_carrier_date`  | Data e horário em que o pedido foi entregue à transportadora |
| `order_delivered_customer_date` | Data e horário em que o pedido foi entregue ao cliente       | 
| `order_estimated_delivery_date` | Data estimada para a entrega do pedido                       |

---

# Descrição das colunas

## 1. `order_id`

Representa o **identificador único de cada pedido**.

Exemplo:

`e481f51cbdc54678b7cc49136f2d6af7`

Essa coluna é importante porque permite identificar cada pedido individualmente e também relacionar essa tabela com outras tabelas da Olist, como:

- itens dos pedidos;
- pagamentos;
- avaliações.

---

## 2. `customer_id`

Representa o **identificador do cliente associado ao pedido**.

Exemplo:

`9ef432eb6251297304e76186b10a928d`

Essa coluna permite relacionar a tabela de pedidos com a tabela de clientes.

É importante observar que `customer_id` não deve ser interpretado diretamente como o identificador permanente de uma pessoa.

Na base completa da Olist também existe a coluna:

`customer_unique_id`

Ela é utilizada para identificar um mesmo consumidor quando ele realiza mais de uma compra.

---

## 3. `order_status`

Indica o **status do pedido**, ou seja, em qual etapa do processo de compra o pedido se encontra ou terminou.

Os possíveis valores encontrados nessa coluna são:

### `delivered`

Significa que o pedido foi **entregue ao cliente**.

Interpretação:

> O processo de entrega foi concluído e o produto chegou ao consumidor.

---

### `shipped`

Significa que o pedido foi **enviado pela transportadora**, mas ainda não possui registro de entrega ao cliente.

Interpretação:

> O produto já foi despachado, mas ainda não consta como entregue.

---

### `canceled`

Significa que o pedido foi **cancelado**.

Interpretação:

> O processo de compra foi interrompido e o pedido não foi concluído normalmente.

O motivo do cancelamento não é informado diretamente nessa tabela.

---

### `unavailable`

Significa que o pedido ficou **indisponível**.

Interpretação:

> O pedido não pôde ser processado normalmente, geralmente por indisponibilidade do item ou impossibilidade de conclusão da operação.

---

### `invoiced`

Significa que o pedido foi **faturado**.

Interpretação:

> O pedido já passou pela etapa de faturamento, mas ainda não consta como enviado pela transportadora.

---

### `processing`

Significa que o pedido está **em processamento**.

Interpretação:

> O pedido está sendo preparado para as próximas etapas do processo de compra e envio.

---

### `approved`

Significa que o pedido foi **aprovado**.

Interpretação:

> A compra já foi aprovada, mas ainda não avançou para as próximas etapas de preparação ou transporte.

---

### `created`

Significa que o pedido foi **criado no sistema**.

Interpretação:

> O pedido foi registrado, mas ainda se encontra em uma etapa inicial.

---

## 4. `order_purchase_timestamp`

Representa a **data e o horário em que o cliente realizou a compra**.

Exemplo:

`2017-10-02 10:56:33`

Interpretação:

> A compra foi realizada em 02/10/2017 às 10:56:33.

Essa coluna pode ser utilizada para analisar:

- quantidade de pedidos por dia;
- quantidade de pedidos por mês;
- quantidade de pedidos por ano;
- horário com maior número de compras;
- sazonalidade;
- evolução das vendas ao longo do tempo.

---

## 5. `order_approved_at`

Representa a **data e o horário em que o pedido foi aprovado**.

Exemplo:

`2017-10-02 11:07:15`

Essa coluna pode ser comparada com `order_purchase_timestamp` para calcular quanto tempo foi necessário para aprovar a compra.

Exemplo de cálculo:

`tempo_aprovacao = order_approved_at - order_purchase_timestamp`

Essa coluna pode possuir valores ausentes em alguns registros.

---

## 6. `order_delivered_carrier_date`

Representa a **data e o horário em que o pedido foi entregue à transportadora responsável pelo envio**.

Exemplo:

`2017-10-04 19:55:00`

Interpretação:

> Nessa data, o pedido saiu da etapa de preparação e passou para a etapa de transporte.

Essa coluna pode ser utilizada para calcular o tempo de preparação do pedido.

Exemplo:

`tempo_preparacao = order_delivered_carrier_date - order_approved_at`

Também pode apresentar valores ausentes quando o pedido não chegou até a etapa de transporte.

---

## 7. `order_delivered_customer_date`

Representa a **data e o horário em que o pedido foi efetivamente entregue ao cliente**.

Exemplo:

`2017-10-10 21:25:13`

Essa coluna permite calcular o tempo total entre a realização da compra e a entrega.

Exemplo:

`tempo_entrega = order_delivered_customer_date - order_purchase_timestamp`

Valores ausentes nessa coluna não necessariamente representam erros.

Por exemplo, pedidos com status `canceled` podem não possuir uma data de entrega, já que nunca chegaram ao cliente.

---

## 8. `order_estimated_delivery_date`

Representa a **data estimada para a entrega do pedido**.

Exemplo:

`2017-10-18 00:00:00`

Essa coluna representa o prazo inicialmente previsto para que a compra chegasse ao cliente.

Pode ser comparada com `order_delivered_customer_date` para verificar se o pedido chegou antes, dentro ou depois do prazo.

Exemplo:

`dias_atraso = order_delivered_customer_date - order_estimated_delivery_date`

### Interpretação

Se:

`dias_atraso > 0`

O pedido chegou **atrasado**.

Se:

`dias_atraso < 0`

O pedido chegou **antes do prazo**.

Se:

`dias_atraso = 0`

O pedido chegou **exatamente na data prevista**.

---

# Fluxo de um pedido

As colunas de data permitem acompanhar o ciclo de vida de uma compra.

```text
order_purchase_timestamp
        ↓
Compra realizada

order_approved_at
        ↓
Compra aprovada

order_delivered_carrier_date
        ↓
Pedido entregue à transportadora

order_delivered_customer_date
        ↓
Pedido entregue ao cliente