# Filip's Homebrew tap

Install the terminal tools:

```sh
brew install filipgutica/tap/annoterm
brew install filipgutica/tap/devps
brew install filipgutica/tap/wtree
brew install filipgutica/tap/filip-stack
```

- [annoterm](https://github.com/filipgutica/annoterm): terminal Markdown review and editing.
- [devps](https://github.com/filipgutica/devps): see which dev servers are running, where they came from, and jump to or stop them. macOS only.
- [wtree](https://github.com/filipgutica/wtree): Git worktree listing, PR state, and cleanup. GitHub CLI (`gh`) is optional for PR state.
- [filip-stack](https://github.com/filipgutica/filip-stack): applies shared agent guidance and setup for Claude and Codex. Uses a separate source checkout on `main` (default: `~/code/filip-stack`).

annoterm and wtree build from source on macOS and Linux; devps builds from source on macOS. Homebrew installs Rust to build annoterm, Node to build and run devps and wtree, and fzf for devps. Formulae use stable GitHub release tags.

filip-stack runs on macOS and Linux with Homebrew's Node. Its dependency-free
launcher installs directly from the release archive. Its formula becomes
available after the first CLI release and generated formula PR merge.

## Releases and formula updates

Each tool owns its version and releases. Conventional squash commits drive release PRs: `fix:` bumps patch, `feat:` bumps minor, and `!` or a `BREAKING CHANGE:` footer bumps major, including before `1.0.0`. Merge a tool's release PR to publish its version.

filip-stack has independent CLI and plugin releases. The updater selects only
stable `cli-vX.Y.Z` releases; plugin `vX.Y.Z` tags do not update the formula.
On the first CLI release, the updater creates `Formula/filip-stack.rb` from
`scripts/templates/filip-stack.rb` and hashes the published archive. Before
that release it leaves the formula absent. The formula PR runs the package
checks on macOS and Linux before it can ship.

This tap checks stable releases every six hours. The **Update formulae** workflow can also be run manually from GitHub Actions. It downloads and hashes each newer release archive, then opens or updates one formula PR. It does not push to `main`.

Bot-created PRs may display **Approve workflows to run**. A maintainer must approve those runs, review the changes, and merge after the formula checks pass. Automation uses each repository's own `GITHUB_TOKEN`; no shared personal token is required.

To refresh installed tools:

```sh
brew update
brew upgrade annoterm devps wtree filip-stack
```

## Local checks

```sh
python3 -B -m unittest discover -s tests
brew audit --strict filipgutica/tap/annoterm filipgutica/tap/devps filipgutica/tap/wtree filipgutica/tap/filip-stack
brew install --build-from-source filipgutica/tap/annoterm filipgutica/tap/devps filipgutica/tap/wtree filipgutica/tap/filip-stack
brew test filipgutica/tap/annoterm filipgutica/tap/devps filipgutica/tap/wtree filipgutica/tap/filip-stack
brew linkage --test filipgutica/tap/annoterm filipgutica/tap/wtree filipgutica/tap/filip-stack
```
