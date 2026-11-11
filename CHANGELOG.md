# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [Unreleased]

### Fixed

- `sale_renting_line_period`: Split a delivered rental order line. The delivered and
  returned quantities are reduced before the ordered quantity, so the `sale_stock`
  quantity check no longer rejects the split.
- `sale_renting_line_period`: Set the line rental return date to the last second of the
  return day. The end of day is calculated in the user timezone.
- `sale_renting_lot_available`: Calculate the available slots by the maximum number of
  overlapping bookings instead of the number of bookings that touch the period
  boundaries.

### Added

- `sale_renting_lot_available`: `_get_max_overlap` and
  `_get_available_placeholder_slot_ids` helpers on `stock.rental.slot`.
