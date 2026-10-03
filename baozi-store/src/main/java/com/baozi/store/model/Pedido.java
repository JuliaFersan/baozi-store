package com.baozi.store.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;

@Entity
public class Pedido {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotNull(message = "clienteId e obrigatorio")
    @Column(nullable = false)
    private Long clienteId;

    @NotNull(message = "produtoId e obrigatorio")
    @Column(nullable = false)
    private Long produtoId;

    @NotNull(message = "quantidade e obrigatoria")
    @Min(value = 1, message = "quantidade minima e 1")
    @Max(value = 1000, message = "quantidade maxima e 1000")
    @Column(nullable = false)
    private Integer quantidade;

    public Pedido() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getClienteId() { return clienteId; }
    public void setClienteId(Long clienteId) { this.clienteId = clienteId; }
    public Long getProdutoId() { return produtoId; }
    public void setProdutoId(Long produtoId) { this.produtoId = produtoId; }
    public Integer getQuantidade() { return quantidade; }
    public void setQuantidade(Integer quantidade) { this.quantidade = quantidade; }
}
