# Documentação do Projeto JuliaMandelbrotConstruction

Bem-vindo à documentação oficial de melhorias e evolução do projeto **JuliaMandelbrotConstruction**. Este repositório é dedicado à exploração, cálculo e renderização matemática de fractais das famílias de Julia e Mandelbrot para polinômios $P_{d,c}(z) = z^d + c$, além de experimentos com dinâmica reversa.

---

## 📌 Sumário da Documentação

Esta pasta `docs/` contém especificações completas, procedimentos práticos e um roteiro estruturado para transformar os scripts do projeto em uma ferramenta científica robusta, modular e rápida:

1. **[01. Manual de Uso por Linha de Comando (CLI)](./01_manual_cli.md)**
   - *Prioridade imediata do projeto.*
   - Como usar todos os recursos do projeto 100% via terminal (sem telas interativas de bloqueio por `input()`).
   - Especificação de argumentos, flags (`--output`, `--no-show`, `--iterations`, etc.), subcomandos e automação em lote (batch scripts).
   - Suporte a ambientes headless (servidores, SSH sem X11).

2. **[02. Roteiro Estruturado de Melhorias (Roadmap)](./02_roteiro_melhorias.md)**
   - Plano de evolução organizado em 5 fases:
     - **Fase 1:** CLI Unificada e Usabilidade (Concluída/Imediata).
     - **Fase 2:** Arquitetura Modular e Desacoplamento (Cálculo vs. Renderização).
     - **Fase 3:** Vetorização com NumPy e Ganho Massivo de Desempenho (de minutos para frações de segundo com `imshow`).
     - **Fase 4:** Testes Automatizados (`pytest`), Tipagem Estática e Qualidade.
     - **Fase 5:** Empacotamento Moderno (`pyproject.toml`) e Distribuição.

3. **[03. Guia Técnico de Refatoração e Otimização](./03_guia_refatoracao_e_codigo.md)**
   - Procedimentos detalhados de código para desenvolvedores.
   - Padrões de parsing seguro de números complexos.
   - Demonstração comparativa de desempenho: loops em Python puro vs. matrizes vetorizadas com NumPy.
   - Como evitar problemas comuns com Matplotlib em servidores e containers.

---

## 🔍 Diagnóstico do Projeto Atual

### Pontos Fortes
- Formulação matemática clara e conceitualmente correta da dinâmica holomorfa de $z^d + c$.
- Inclusão de métodos diretos e reversos (órbita direta, dinâmica reversa estocástica e iteração reversa de círculos).
- Imagens geradas com alto apelo visual e esquemas de cores por tempo de escape.

### Oportunidades Críticas de Melhoria
1. **Dependência de `input()` interativo:**
   - Anteriormente, todos os scripts exigiam digitação manual no terminal a cada execução.
   - Impedia automação, pipelines, criação de animações ou execução em servidores remotos.
   - *Solução:* Interface CLI completa e compatibilidade com argumentos via linha de comando.
2. **Gargalo de Desempenho (Loops puros e Scatter Plot):**
   - Os cálculos eram feitos com dois loops `for` aninhados em Python ponto a ponto.
   - A plotagem acumulava listas de coordenadas e chamava `plt.plot(..., 'o', markersize=0.1)` 8 vezes sobre milhares de pontos, consumindo muita memória e tempo de CPU.
   - *Solução:* Vetorização de matrizes booleanas com NumPy e renderização direta com `plt.imshow()`.
3. **Acoplamento e Duplicação:**
   - Lógica de cálculo matemático misturada com chamadas diretas de `plt.plot()` e `input()`.
   - A função `exibir_ou_salvar()` estava copiada em múltiplos arquivos.
   - O arquivo `iteracoesReversasCirculo.py` executava código imediatamente no nível do módulo (sem guarda `if __name__ == "__main__":`).
   - *Solução:* Criação de módulos utilitários e separação clara de responsabilidades.

---

## 🚀 Como Começar Imediatamente

Para começar a usar o projeto via linha de comando agora mesmo, consulte o **[Manual de Uso por Linha de Comando](./01_manual_cli.md)**.
