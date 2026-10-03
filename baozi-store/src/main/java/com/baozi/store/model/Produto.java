package com.baozi.store.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.*;
import java.math.BigDecimal;

@Entity
public class Produto {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "nome e obrigatorio")
    @Size(max = 100, message = "nome deve ter no maximo 100 caracteres")
    @Column(nullable = false, length = 100)
    private String nome;

    @NotNull(message = "preco e obrigatorio")
    @Positive(message = "preco deve ser maior que zero")
    @Digits(integer = 8, fraction = 2, message = "preco invalido")
    @Column(nullable = false, precision = 10, scale = 2)
    private BigDecimal preco;

    @NotNull(message = "estoque e obrigatorio")
    @Column(nullable = false)
    private Boolean estoque;

    public Produto() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }
    public BigDecimal getPreco() { return preco; }
    public void setPreco(BigDecimal preco) { this.preco = preco; }
    public Boolean getEstoque() { return estoque; }
    public void setEstoque(Boolean estoque) { this.estoque = estoque; }
}
