package com.baozi.store.controller;

import com.baozi.store.model.Produto;
import com.baozi.store.repository.PedidoRepository;
import com.baozi.store.repository.ProdutoRepository;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/produtos")
public class ProdutoController {

    private final ProdutoRepository repository;
    private final PedidoRepository pedidoRepository;

    public ProdutoController(ProdutoRepository repository, PedidoRepository pedidoRepository) {
        this.repository = repository;
        this.pedidoRepository = pedidoRepository;
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Produto criar(@Valid @RequestBody Produto produto) {
        produto.setId(null);
        return repository.save(produto);
    }

    @GetMapping
    public List<Produto> listar() {
        return repository.findAll();
    }

    @GetMapping("/{id}")
    public Produto buscar(@PathVariable Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Produto nao encontrado"));
    }

    @PutMapping("/{id}")
    public Produto atualizar(@PathVariable Long id, @Valid @RequestBody Produto dados) {
        Produto existente = buscar(id);
        existente.setNome(dados.getNome());
        existente.setPreco(dados.getPreco());
        existente.setEstoque(dados.getEstoque());
        return repository.save(existente);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void apagar(@PathVariable Long id) {
        buscar(id);
        if (pedidoRepository.existsByProdutoId(id)) {
            throw new ResponseStatusException(HttpStatus.CONFLICT, "Produto possui pedidos e nao pode ser apagado");
        }
        repository.deleteById(id);
    }
}
