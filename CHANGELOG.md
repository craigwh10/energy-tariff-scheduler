# Changelog

All notable changes to this project will be documented in this file.

Format: [https://gist.github.com/juampynr/4c18214a8eb554084e21d6e288a18a2c](https://gist.github.com/juampynr/4c18214a8eb554084e21d6e288a18a2c)

## [0.0.5] - 2025-01-02

### Added

- Retry logic added to Octopus Agile API (this isn't failsafe as sometimes it does fail to return results over long periods)
- Full schedule is now logged under `INFO` with price, time and what action it ran

### Changed

- Removed `runners` from module, now just `runner`

### Fixed

- Made the initial schedule job run if the current time is within 15 minutes of the job execution time
- Users now have to provide an API key for Octopus runners, this is to get the accurate tariff, previously assumed a single tariff that soon became unavailable.

## [0.0.6] - 2025-01-03

### Added

- Intelligent Go and Regular Go tariff support

### Changed

### Fixed

## [0.0.7] - 2025-01-03

### Added

### Changed

- Removed interpolations, jobs for Go and Intelligent Go now only trigger during price boundaries

### Fixed