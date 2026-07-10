# Changelog

## 0.6.0

### Security

- **Critical: closed an arbitrary-code-execution vulnerability.** Task metadata
  was loaded with the unsafe `yaml.Loader`, so a crafted `.pdpp_task.yaml`
  executed arbitrary code the moment any `pdpp` command touched the project.
  Loading now uses a restricted loader that reconstructs only the known pdpp
  task types and `dep_dataclass`, and rejects every other object tag. Existing
  project files written by older versions still load.

### Added

- `pdpp migrate` rewrites a project's `.pdpp_task.yaml` files into a new
  schema-versioned, plain-dict format that contains no Python object tags. It
  is idempotent.
- Per-project materialization mode (`copy` by default, or `hardlink` /
  `symlink`), configurable with the `PDPP_MATERIALIZE_MODE` environment
  variable or `[tool.pdpp] materialize_mode` in a project `pdpp.toml`.
- `pdpp --version`.
- A pytest test suite and a GitHub Actions CI workflow.
- `py.typed` marker and single-sourced `pdpp.__version__`.

### Changed

- **Task inputs are now copied, not hard-linked, by default.** This removes the
  silent two-way aliasing between an upstream `output/` file and a downstream
  `input/` file, so editing an input no longer rewrites the upstream output.
- Materialization is portable: hard-link and symlink modes fall back to a copy
  across filesystems (EXDEV) and on drives that cannot support links, instead
  of crashing.
- Rigging no longer wipes a task's whole `input/` directory. Only declared
  dependency files are refreshed; unmanaged user files are preserved.
- Terminal task outputs (with no downstream consumer) are tracked, so deleting
  one now triggers regeneration instead of being reported up-to-date.
- Running an enabled task that depends on a disabled upstream task now fails
  with a clear message instead of silently using stale linked data.
- Metadata writes are atomic (temp file + replace), so a crash mid-write cannot
  truncate `.pdpp_task.yaml`.
- CLI errors are clean: running outside a project, cancelling a prompt, or
  running with non-interactive stdin now exit with a message instead of a raw
  traceback.

### Removed

- Unused runtime dependencies `pandas`, `toml`, and the `graphviz` Python
  package (rendering uses `pydot` plus the system `dot` binary).
- Dead module `old_graph_dependencies.py` and leftover debug prints.
- Legacy `black` / `isort` / `flake8` configuration in favor of `ruff`.
