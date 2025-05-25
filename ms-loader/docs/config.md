# Configuration Guide

## Environment Variables

### PostgreSQL Configuration
```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=cdr_db
POSTGRES_USER=cdr_user
POSTGRES_PASSWORD=cdr_password
```

### Kafka Configuration
```env
KAFKA_SERVERS=localhost:9092
KAFKA_TOPIC=cdr-records
```

## File Formats

### CSV Format
```csv
source,destination,starttime,service,usage
1001,2001,2025-05-25T14:30:00,voice,12.5
```

### JSON Format
```json
[{
  "source": "1001",
  "destination": "2001",
  "starttime": "2025-05-25T14:30:00",
  "service": "voice",
  "usage": 12.5
}]
```

### XML Format
```xml
<records>
  <record>
    <source>1001</source>
    <destination>2001</destination>
    <starttime>2025-05-25T14:30:00</starttime>
    <service>voice</service>
    <usage>12.5</usage>
  </record>
</records>
```

### YAML Format
```yaml
- source: "1001"
  destination: "2001"
  starttime: "2025-05-25T14:30:00"
  service: "voice"
  usage: 12.5
```