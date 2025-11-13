# Contracts Directory

**Date**: 2025-01-27  
**Feature**: 001-aion-simulation

## Overview

This directory contains interface contracts and API specifications for the AION simulation application. Since this is a Streamlit web application (not a REST API), contracts define module interfaces, data formats, and component usage patterns.

## Files

- **module-interfaces.md**: Defines function signatures, class interfaces, and contracts between modules
- **README.md**: This file

## Contract Types

1. **Module Interfaces**: Function signatures and class APIs for core models, visualization, and UI components
2. **Data Formats**: Structure of data passed between modules (SimulationParameters, VisualizationData)
3. **Error Handling**: Expected exception types and error handling patterns
4. **Performance**: Performance requirements and guarantees

## Usage

These contracts serve as:
- **Implementation Guide**: Developers implement modules according to these interfaces
- **Testing Reference**: Tests verify modules conform to contracts
- **Documentation**: Clear API documentation for module integration

## Notes

For a traditional REST API, this directory would contain OpenAPI/Swagger schemas. For a Streamlit application, module interfaces and data format contracts are the appropriate abstraction level.

