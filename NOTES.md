# Estado — Gate 1 catálogo e apresentação, 2026-10-28

**Estado:** implementação local isolada no branch
`feat/gate1-portfolio-catalog`, baseada em
`improve/portfolio-project-paths-oct26`. Gate 1 aprovado para commit, push e
PR draft; merge, GitHub Pages, alteração de visibilidade e alterações de
repositórios de produto continuam excluídos.

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

**Follow-up PR #5:** a homepage foi alinhada com WorkAttest em vez de Public
Repo Audit. A página WorkAttest declara o escopo MVP/source-only e os limites
de custódia de chaves e comandos definidos pelo operador. As regressões agora
cobrem a coerência entre catálogo, cartões, CTAs, estados e seleção da homepage.

**Dependência futura:** o PR #4 permanece draft e conserva Public Repo Audit
no diagrama da sua descrição. Não é alterado neste trabalho; deve ser
reconciliado com a seleção aprovada depois da integração do PR #5.

**Próximo passo:** rever o PR #5 atualizado sem o marcar ready. Merge e
publicação continuam a requerer autorização específica.
