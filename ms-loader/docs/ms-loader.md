# CDR Loader Service

A microservice for loading and processing Call Detail Records (CDR) from multiple file formats into PostgreSQL and Kafka.

## Features

- Multi-format support (CSV, JSON, XML, YAML)
- PostgreSQL storage with duplicate detection
- Kafka message publishing
- Scheduled processing
- Docker support

## Prerequisites

- Python 3.13+
- PostgreSQL 15+
- Apache Kafka
- Docker and Docker Compose

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd ms-loader
```

2. Create and configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Start the services:
```bash
docker-compose up -d
```

4. Run the application:
```bash
python -m app.main
```

## Configuration

The service uses environment variables for configuration. See [Configuration Guide](docs/config.md) for details.

## Architecture

The service follows a modular architecture:
- File Parsers: Handle different input formats
- Database Layer: PostgreSQL storage with duplicate detection
- Message Queue: Kafka integration
- Scheduler: Periodic processing

## Documentation

- [Setup Guide](docs/setup.md)
- [Configuration Guide](docs/config.md)

## License

MIT License - See LICENSE file for details