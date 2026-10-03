package com.baozi.store.model;

import jakarta.persistence.*;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.PastOrPresent;
import jakarta.validation.constraints.Size;
import java.time.LocalDate;

@Entity
public class Cliente {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @NotBlank(message = "nome e obrigatorio")
    @Size(max = 100, message = "nome deve ter no maximo 100 caracteres")
    @Column(nullable = false, length = 100)
    private String nome;

    @PastOrPresent(message = "clienteDesde nao pode ser data futura")
    private LocalDate clienteDesde;

    public Cliente() {}

    @PrePersist
    void definirDataPadrao() {
        if (clienteDesde == null) {
            clienteDesde = LocalDate.now();
        }
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getNome() { return nome; }
    public void setNome(String nome) { this.nome = nome; }
    public LocalDate getClienteDesde() { return clienteDesde; }
    public void setClienteDesde(LocalDate clienteDesde) { this.clienteDesde = clienteDesde; }
}
