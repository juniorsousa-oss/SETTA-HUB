# PADRÃO VISUAL SETTA

## REFERÊNCIA OFICIAL ATUAL

Até nova decisão, o aplicativo **FECHAMENTO-MENSAL** é a referência visual e estrutural para todos os aplicativos internos SETTA.

Novos aplicativos e evoluções dos aplicativos existentes devem convergir gradualmente para essa base, preservando as regras de negócio de cada sistema.

## PRINCÍPIOS

1. **TÍTULOS EM CAIXA ALTA**
   - Títulos de páginas, módulos, cartões e cabeçalhos de tabelas devem usar caixa alta.
   - Textos operacionais, campos e mensagens podem manter capitalização normal quando isso favorecer a leitura.

2. **MÓDULOS BEM SEPARADOS**
   - Usar faixas de seção no padrão do FECHAMENTO-MENSAL:
     - fundo branco;
     - borda leve;
     - barra lateral escura;
     - kicker numérico/vermelho;
     - título forte em caixa alta.
   - Separar módulos por divisores discretos, evitando blocos soltos visualmente.

3. **MENOS POLUIÇÃO VISUAL**
   - Mostrar somente a informação necessária para decidir ou executar uma ação.
   - Evitar legendas e textos explicativos longos permanentes.
   - Instruções detalhadas devem ficar em ajuda, tooltip, expander ou documentação.
   - Estados vazios e alertas devem ser curtos e objetivos.

4. **CARTÕES**
   - Fundo branco, borda cinza clara, cantos arredondados e sombra leve.
   - Indicadores devem priorizar leitura rápida.
   - Evitar excesso de cores; cor deve indicar estado, prioridade ou exceção.

5. **TABELAS E PLANILHAS**
   - Container branco com borda leve, cantos arredondados e sombra discreta.
   - Cabeçalhos em caixa alta.
   - Nomes de colunas objetivos.
   - Evitar colunas técnicas quando não agregam valor operacional.
   - Manter filtros próximos da tabela e sem textos explicativos redundantes.

6. **DESEMPENHO É REQUISITO DE LAYOUT**
   - Não carregar bases grandes no startup quando não forem necessárias.
   - Usar lazy loading, cache e invalidação seletiva.
   - Evitar consultas repetidas por rerun do Streamlit.
   - Buscar primeiro status/metadados leves e carregar payload completo somente quando necessário.
   - Não substituir componentes nativos eficientes por HTML pesado sem necessidade.

7. **RESPONSIVIDADE**
   - O mesmo fluxo deve funcionar em desktop e celular.
   - Grids devem quebrar progressivamente sem comprometer leitura e ações.

## PALETA BASE

- Fundo do aplicativo: `#f4f7fb`
- Superfícies/cartões: `#ffffff`
- Texto principal: `#111827`
- Texto secundário: `#667085`
- Bordas: `#dfe3e8` / `#e5e8ee`
- Destaque SETTA para identificação de seção: `#ef4444`
- Verde positivo: `#166534`
- Vermelho negativo/alerta: `#b91c1c`

## REGRA DE EVOLUÇÃO

O padrão será refinado continuamente. Enquanto não houver uma nova referência formal, qualquer novo aplicativo SETTA ou alteração visual relevante deve usar o **FECHAMENTO-MENSAL** como base de comparação antes da implementação.
