# Estado — revisão de percursos de projetos, 2026-10-26

**Estado:** alteração local no branch `improve/portfolio-project-paths-oct26`.
Sem push, merge, GitHub Pages ou alteração de visibilidade.

- Criada `projects/workattest/index.html`, uma página inglesa para o projeto
  original WorkAttest: problema, público, funcionalidades documentadas,
  limitações, autoria e ligação para o código.
- Atualizados sitemap, README e regressão estrutural para seis páginas de
  projeto. O catálogo público atual permanece inalterado nesta ronda; por isso
  o URL WorkAttest não deve ser usado por CriaTek até este portal ser publicado.
- Factos confirmados em leitura dos metadados públicos do GitHub: WorkAttest,
  Quality Docs Validator, Public Repo Audit e Agent Skill Quality Gate não são
  forks nem estão arquivados. Beyond Test Coverage é tratado fora da seleção
  CriaTek como fork.

**Verificado:** `python tests/validate_portal.py` passou para 10 documentos
HTML; `node --check assets/catalog.js` passou; `git diff --check` limpo.

**Próximo passo:** revisão humana e publicação independente deste portal antes
de ligar `https://migmcc.github.io/projects/workattest/` a partir de CriaTek.
