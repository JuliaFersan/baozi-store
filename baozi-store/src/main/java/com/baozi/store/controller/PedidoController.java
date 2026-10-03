package com.baozi.store.controller;

import com.baozi.store.model.Pedido;
import com.baozi.store.repository.ClienteRepository;
import com.baozi.store.repository.PedidoRepository;
import com.baozi.store.repository.ProdutoRepository;
import jakarta.validation.Valid;
import java.util.List;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.server.ResponseStatusException;

@RestController
@RequestMapping("/pedidos")
public class PedidoController {

    private final PedidoRepository repository;
    private final ClienteRepository clienteRepository;
    private final ProdutoRepository produtoRepository;

    public PedidoController(PedidoRepository repository, ClienteRepository clienteRepository,
                            ProdutoRepository produtoRepository) {
        this.repository = repository;
        this.clienteRepository = clienteRepository;
        this.produtoRepository = produtoRepository;
    }

    // Integridade referencial: cliente e produto precisam existir e o produto precisa ter estoque
    private void validarReferencias(Pedido pedido) {
        if (!clienteRepository.existsById(pedido.getClienteId())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "clienteId inexistente");
        }
        var produto = produtoRepository.findById(pedido.getProdutoId())
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.BAD_REQUEST, "produtoId inexistente"));
        if (!Boolean.TRUE.equals(produto.getEstoque())) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "Produto sem estoque");
        }
    }

    @PostMapping
    @ResponseStatus(HttpStatus.CREATED)
    public Pedido criar(@Valid @RequestBody Pedido pedido) {
        pedido.setId(null);
        validarReferencias(pedido);
        return repository.save(pedido);
    }

    @GetMapping
    public List<Pedido> listar() {
        return repository.findAll();
    }

    @GetMapping("/{id}")
    public Pedido buscar(@PathVariable Long id) {
        return repository.findById(id)
                .orElseThrow(() -> new ResponseStatusException(HttpStatus.NOT_FOUND, "Pedido nao encontrado"));
    }

    @PutMapping("/{id}")
    public Pedido atualizar(@PathVariable Long id, @Valid @RequestBody Pedido dados) {
        Pedido existente = buscar(id);
        validarReferencias(dados);
        existente.setClienteId(dados.getClienteId());
        existente.setProdutoId(dados.getProdutoId());
        existente.setQuantidade(dados.getQuantidade());
        return repository.save(existente);
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void apagar(@PathVariable Long id) {
        buscar(id);
        repository.deleteById(id);
    }
}
