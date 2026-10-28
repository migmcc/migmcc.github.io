# Estado — Gate 1 catálogo e apresentação, 2026-10-28

**Estado:** Gate 1 foi integrado em `main` no commit
`3b59d95394ea5374f66ccd8910a891f4a7a36c9b` e GitHub Pages foi validado pelo
titular. Gate 2 decorre apenas localmente em `feat/gate2-pr4-reconcile`,
partindo dessa `main`; não há commit, push, merge ou deploy autorizado.

- Criado `assets/catalog-data.js` como registo estruturado das cinco entradas
  aprovadas: Quality Docs Validator, Agent Skill Quality Gate, ProjectPilot,
  Agent Desk e WorkAttest.
- Atualizada a grelha de `/projects/`: Public Repo Audit deixou de ser
  destacado; WorkAttest passou a constar como MVP source-only; release estável,
  tag estável e MVP são distinguíveis visualmente e nos CTAs.
- Os CTAs apontam para Releases/tags GitHub concretas ou fonte/documentação;
  nenhum source archive é apresentado como download de aplicação.
- A regressão estrutural cobre o catálogo, modos de distribuição, exclusão de
  Public Repo Audit, cinco estados visíveis e os hooks do refinamento visual.
  O README explica a nova fonte de dados e a regra de não chamar download a
  uma tag/fonte.
- Após revisão humana desktop e mobile a 390 px, foi reduzida a hero do
  catálogo, aligeirado o guia de releases e agrupadas as ações dos cartões:
  `Explore project` é a ação primária; a release/tag/source é secundária.
  Acentos de cor discretos distinguem qualidade, workflow e traceability sem
  imagens nem assets externos.

**Verificado:** revisão humana desktop e mobile 390 px, cartões, foco de
teclado, pesquisa e contagem; `python tests/validate_portal.py` passou para
10 documentos; `node --check assets/catalog-data.js`; `node --check
assets/catalog.js`; e `git diff --check` sem erros.

**Decisões pendentes:** corrigir o README do AgentDesk no repositório próprio;
resolver a identidade CriaTek vs pessoal de Public Repo Audit antes de qualquer
entrada futura; confirmar visualmente as dimensões 1440 × 900 e 390 × 844.

**Gate 2 / PR #4:** o PR #4 continua draft (`f7a3f61`) e está `DIRTY` contra a
`main` atual. Reaproveitar apenas o mapa de apresentação e a alternativa móvel:
substituir Public Repo Audit por WorkAttest, preservar os metadados Open Graph
já existentes na `main` e evitar a reformatação ampla do PR antigo. O catálogo,
CTAs, estados e avisos da página WorkAttest não são alterados.

**Gate 2 final:** a revisão humana desktop e mobile (390 px) aprovou o mapa e
os cartões móveis. O título partilhado da secção passou para “Five focused
tools. One shared engineering approach.”; o SVG não contém esse título e a
alternativa móvel herda o mesmo `h2` da secção. As regressões confirmam os
cinco projetos, a ausência de Public Repo Audit e o aviso WorkAttest
MVP/source-only preservado.

**Próximo passo:** criar um novo PR a partir desta branch após autorização e
depois fechar ou substituir o PR #4 original. Merge e publicação continuam a
requerer autorização específica.
