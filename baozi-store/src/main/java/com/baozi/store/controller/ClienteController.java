package com.baozi.store.controller;

import com.baozi.store.model.Cliente;
import com.baozi.store.repository.ClienteRepository;
import com.baozi.store.repository.PedidoRepository;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/clientes")
public class ClienteController {

    private final ClienteRepository repository;
    private final PedidoRepository pedidoRepository;

    public ClienteController(ClienteRepository repository, PedidoRepository pedidoRepository) {
        this.repository = repository;
        this.pedidoRepository = pedidoRepository;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Cliente criar(@Valid @RequestBody Cliente cliente) {
        cliente.setId(null); // impede que o chamador escolha o proprio id
        return repository.save(cliente);
    }

    @GetMapping
    public List<Cliente> listar() {
        return repository.findAll();
    }

    @GetMapping("/{id}")
    public Cliente buscar(@PathVariable Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Cliente nao encontrado"));
    }

    @PutMapping("/{id}")
    public Cliente atualizar(@PathVariable Long id, @Valid @RequestBody Cliente dados) {
        Cliente existente = buscar(id);
        existente.setNome(dados.getNome());
        if (dados.getClienteDesde() != null) {
            existente.setClienteDesde(dados.getClienteDesde());
        }
        return repository.save(existente);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void apagar(@PathVariable Long id) {
        buscar(id);
        if (pedidoRepository.existsByClienteId(id)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Cliente possui pedidos e nao pode ser apagado");
        }
        repository.deleteById(id);
    }
}
