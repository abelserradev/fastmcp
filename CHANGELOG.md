# Changelog

All notable changes to this project will be documented in this file.

The format is based on Keep a Changelog, and this project adheres to Semantic Versioning.

Repository: https://bitbucket.org/venelife/integration-seguros-mercantil

## [Unreleased]
- No changes yet.

## [0.2.0] - 2025-11-18

### Added
- Pasarela de Pago module v2 with enhanced schemas and payment processing APIs (`PasarelaPagoMS v2`). [0383e66](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/0383e66)
- Multiple versioned routers wired (Integration_SM v1–v5; PasarelaPagoMS v1–v2) in central app. (via cumulative commits/merges)
- Timezone handling in application startup. [c433ea6](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/c433ea6)

### Changed
- Logging module adjusted to reduce noise; router tags and summaries updated for Pasarela de Pago. [df9762a](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/df9762a)
- Logging subsystem prepared to support MongoDB sink collection for integrator logs (see utils v2). [95859aa](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/95859aa)
- General dependency and documentation updates via periodic merges from `develop`. [c8c474b](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/c8c474b), [6f25c45](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/6f25c45)

### Fixed
- Correct handling of `cd_persona_med` to avoid treating the string "None" as a value and to properly manage `None`. [44d9c64](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/44d9c64), [5907c2d](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/5907c2d), [6e7279e](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/6e7279e)

### Notes
- SemVer bump: minor. New user‑facing features (PasarelaPagoMS v2) without known breaking changes.

## [0.1.0] - 2024-07-01

### Added
- Initial FastAPI application with versioned endpoints for Seguros Mercantil integration: crear/emitir/consultar póliza, crear/consultar persona, incluir anexo. [af10887](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/af10887), [ed723fb](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/ed723fb), [968e9f9](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/968e9f9), [7805b70](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/7805b70), [d7d7430](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/d7d7430), [343c7e0](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/343c7e0)
- API key support and proper `dd/mm/yyyy` date formatting. [129bc22](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/129bc22)
- App template and initial project structure. [c51b854](https://bitbucket.org/venelife/integration-seguros-mercantil/commits/c51b854)

<!-- Links -->
[Unreleased]: https://bitbucket.org/venelife/integration-seguros-mercantil/branches/compare/HEAD..0.2.0
[0.2.0]: https://bitbucket.org/venelife/integration-seguros-mercantil/commits/tag/0.2.0
[0.1.0]: https://bitbucket.org/venelife/integration-seguros-mercantil/commits/tag/0.1.0
