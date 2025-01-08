# Introduction

All notable changes to this project will be documented in this file.

If a version moves in major versions for example from `0.0.0` to `1.0.0` please be sure to read the change log to understand what has changed with a remedy to fix it, a major version bump means that the things you interact with are no longer backwards compatible between versions.

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

## [0.0.8] - 2025-01-08

### Added

### Changed

### Fixed

- Product tariff matching is now using the convention rather than fuzzy matching, as to support products endpoint not returning products with `valid_to` in the future.

# Reference

This changelog is following the format shown in <a href="https://gist.github.com/juampynr/4c18214a8eb554084e21d6e288a18a2c" target="_blank">https://gist.github.com/juampynr/4c18214a8eb554084e21d6e288a18a2c</a>