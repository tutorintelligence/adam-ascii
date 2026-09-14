# CHANGELOG


## v0.4.1 (2026-09-14)

### Bug Fixes

- Rename the style console script to adam-ascii-style
  ([`373ec6e`](https://github.com/tutorintelligence/adam-ascii/commit/373ec6eba2180adcc69f7281160308273a2c0836))

A console script named `style` lands in the bin/ of every venv that installs this package, where it
  races the host project's own `style` script. The stub also points at poetry_scripts, which the
  wheel does not ship.

Refs SW-6487

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>

Claude-Session: https://claude.ai/code/session_01LPonKA7omwBYKhbTG82K76

### Continuous Integration

- Release with semantic-release v9 and checkout v4
  ([`4fd55ed`](https://github.com/tutorintelligence/adam-ascii/commit/4fd55ed6680b2d8cdb701a4e0cd9f2bbdb157d51))

semantic-release v8.0.0 builds its Docker image at run time, and the image's `apt-get install
  git-lfs` now 404s on the retired Debian bullseye mirror, so the release job fails before it
  starts. This matches the workflow tcp-modbus-aio releases with.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>

Claude-Session: https://claude.ai/code/session_019rXa4WhQJqVi8vQzLhEbou


## v0.4.0 (2024-04-21)

### Features

- Rename pypi package to adam-ascii
  ([`28eb3d1`](https://github.com/tutorintelligence/adam-ascii/commit/28eb3d182139fe8039e56c7fad3701e54f5d169c))


## v0.3.1 (2023-11-29)

### Bug Fixes

- Repr for errors
  ([`17822a8`](https://github.com/tutorintelligence/adam-ascii/commit/17822a877709e8620a78cf692073a14a83782a54))


## v0.3.0 (2023-09-13)

### Features

- Send_and_receive is atomic
  ([`39e2fa3`](https://github.com/tutorintelligence/adam-ascii/commit/39e2fa3d5990a7d99eaa2afbb216e752d3d4afbf))


## v0.2.0 (2023-08-21)

### Features

- Enable high speed analog integration
  ([`197ccba`](https://github.com/tutorintelligence/adam-ascii/commit/197ccbad6831db7f030462ddc468ab6d996ad7c6))


## v0.1.4 (2023-08-07)

### Bug Fixes

- Py.typed file to propogate hints
  ([`a85c2dc`](https://github.com/tutorintelligence/adam-ascii/commit/a85c2dcc6244a55a61a4692fc25571ed3048fda8))

### Chores

- Add pypi to readme
  ([`1f0a7db`](https://github.com/tutorintelligence/adam-ascii/commit/1f0a7dbcd2ec8a30cc8905f17d0f08040282ce27))


## v0.1.3 (2023-08-07)

### Bug Fixes

- Updates to poetry configuration
  ([`51cb567`](https://github.com/tutorintelligence/adam-ascii/commit/51cb567d332befadca1fc656bf49189553694049))


## v0.1.2 (2023-08-07)

### Bug Fixes

- Trigger a version bump
  ([`5470820`](https://github.com/tutorintelligence/adam-ascii/commit/54708204fbdff430c2b43cc5a0be23be0ce84831))

### Chores

- More flexible interface
  ([`0244fb4`](https://github.com/tutorintelligence/adam-ascii/commit/0244fb4cc61024a71a3dda761798b64b6afafc30))

- Refactor to object inerface
  ([`f0de1c2`](https://github.com/tutorintelligence/adam-ascii/commit/f0de1c2e432ded96b75b96401032a57d797f1c7c))


## v0.1.1 (2023-08-07)

### Bug Fixes

- Try fixing long description field for pypy upload
  ([`feefcfd`](https://github.com/tutorintelligence/adam-ascii/commit/feefcfdffd61e14cb3f5bbe4dcaec2ee351e97ea))

### Chores

- More flexible interface
  ([`4fbd036`](https://github.com/tutorintelligence/adam-ascii/commit/4fbd03656afadc859f624f88e7e455d3b9596efb))


## v0.1.0 (2023-08-07)

### Features

- Initial commit
  ([`f4f244b`](https://github.com/tutorintelligence/adam-ascii/commit/f4f244b707136758175baf0ace424d4fca905677))
