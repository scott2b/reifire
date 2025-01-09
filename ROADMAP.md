# Reifire 🔥 project roadmap


## Data specification

- [ ] Complete a detailed data specification in DATASPEC.md


## Articulation

- [x] Implement articulation module

### Articulation Module Improvements

#### Attribute Handling Abstraction
- [x] Remove hard-coded attributes (e.g., "scary-cute", "color scheme")
- [x] Consolidate redundant style-related conditions
- [x] Create extensible attribute type system
- [x] Implement generic attribute handler interface

#### Relationship Handling Abstraction
- [x] Create relationship handler protocol
- [x] Implement handlers for basic relationship types (references, contains, compares)
- [x] Add support for relationship properties
- [x] Create extensible relationship type system
- [x] Move relationship text generation to dedicated handlers
  - [x] Move text pattern handling to RelationshipType class
  - [x] Add support for complex text generation patterns
  - [x] Make text generation configurable through templates
  - [x] Support custom text formatters per relationship type

#### String Pattern Management
- [x] Create unified pattern replacement system
- [x] Remove redundant style-related replacements
- [x] Implement configurable text transformation rules
- [x] Remove hard-coded special cases

#### Structural Flexibility
- [ ] Remove rigid object/modifier/attribute assumptions
- [ ] Implement flexible property structure handling
- [ ] Create generic relationship type system
- [ ] Support custom object structures

#### Text Generation System
- [ ] Create configurable prefix system
- [ ] Implement flexible sentence structure
- [ ] Support multiple output formats
- [ ] Add customizable text assembly rules

#### Configuration and Customization
- [ ] Implement template-based text generation
- [ ] Create attribute registry system
- [ ] Add support for custom formatters
- [ ] Create environment-specific configuration system
- [ ] Support external pattern definitions

#### Pattern-based Assembly
- [ ] Define formal grammar for text assembly
- [ ] Implement configurable joining rules
- [ ] Support multiple output styles
- [ ] Create pattern validation system

- [x] Implement attribute handler system
  - Convert hard-coded attributes into a flexible handler system
  - Add support for different attribute types
  - Add proper error handling

- [x] Improve relationship handling
  - Add relationship type system
  - Implement handlers for different relationship types
  - Add support for relationship properties

- [x] Fix over-specification issues
  - Remove unnecessary handlers
  - Improve pattern transformations
  - Fix attribute order and formatting

- [x] Clean up text transformations
  - Add pattern manager for consistent text transformations
  - Fix issues with duplicate words
  - Improve handling of special cases

- [ ] Add support for more complex relationships
  - Support for nested relationships
  - Better handling of relationship chains
  - More flexible property handling

- [ ] Improve error handling and validation
  - Add input validation for reified structures
  - Better error messages for invalid inputs
  - Graceful handling of edge cases

- [ ] Add extensibility features
  - Make it easier to add new handlers
  - Support for custom pattern transformations
  - Plugin system for third-party extensions






