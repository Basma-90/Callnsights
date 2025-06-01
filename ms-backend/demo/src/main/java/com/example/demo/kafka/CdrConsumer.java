package com.example.demo.kafka;
import com.example.demo.model.Cdr;
import com.example.demo.repository.CdrRepository;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;

@Service
public class CdrConsumer {
    
    private static final Logger logger = LoggerFactory.getLogger(CdrConsumer.class);
    
    @Autowired
    private CdrRepository cdrRepository;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @PostConstruct
    public void init() {
        logger.info("CdrConsumer initialized and ready to receive messages from Kafka topic 'cdr-records'");
    }
    
    @KafkaListener(
        topics = "cdr-records",
        groupId = "new-consumer-group-2025"
    )
    public void consume(String message) {
        logger.info("Received message from Kafka: {}", message);
        
        try {
            CdrMessage cdrMessage = objectMapper.readValue(message, CdrMessage.class);
            logger.info("Parsed message to CdrMessage object: source={}, destination={}", 
                cdrMessage.getSource(), cdrMessage.getDestination());
            
            Cdr cdr = new Cdr();
            cdr.setSource(cdrMessage.getSource());
            cdr.setDestination(cdrMessage.getDestination());
            
            String startTimeStr = cdrMessage.getStarttime();
            if (startTimeStr != null && !startTimeStr.isEmpty()) {
                try {
                    cdr.setStartTime(LocalDateTime.parse(startTimeStr));
                    logger.info("Successfully parsed date: {}", startTimeStr);
                } catch (Exception e) {
                    logger.error("Failed to parse date: {}. Error: {}", startTimeStr, e.getMessage());
                    cdr.setStartTime(LocalDateTime.now());
                }
            } else {
                logger.warn("Start time is null or empty in the incoming message");
                cdr.setStartTime(LocalDateTime.now());
            }
            
            if (cdrMessage.getService() != null) {
                try {
                    String serviceUpper = cdrMessage.getService().toUpperCase();
                    cdr.setServiceType(Cdr.ServiceType.valueOf(serviceUpper));
                    logger.info("Mapped service '{}' to enum {}", cdrMessage.getService(), serviceUpper);
                } catch (IllegalArgumentException e) {
                    logger.warn("Unknown service type: '{}'. Using default VOICE", cdrMessage.getService());
                    cdr.setServiceType(Cdr.ServiceType.VOICE);
                }
            } else {
                logger.warn("Service type is null. Using default VOICE");
                cdr.setServiceType(Cdr.ServiceType.VOICE);
            }
            
            cdr.setUsage(cdrMessage.getUsage() != null ? cdrMessage.getUsage() : 0.0);
            cdr.setFileName(cdrMessage.getFileName());
            
            logger.info("Prepared CDR entity for saving: {}", cdr);
            
            Cdr savedCdr = cdrRepository.save(cdr);
            logger.info("Successfully saved CDR record with ID: {}", savedCdr.getId());
            
        } catch (Exception e) {
            logger.error("Error processing Kafka message: {}", e.getMessage(), e);
        }
    }
    
    static class CdrMessage {
        private String source;
        private String destination;
        private String starttime;
        private String service;
        private Double usage;
        
        @JsonProperty("file_name")
        private String fileName;
        
        public String getSource() { return source; }
        public void setSource(String source) { this.source = source; }
        
        public String getDestination() { return destination; }
        public void setDestination(String destination) { this.destination = destination; }
        
        public String getStarttime() { return starttime; }
        public void setStarttime(String starttime) { this.starttime = starttime; }
        
        public String getService() { return service; }
        public void setService(String service) { this.service = service; }
        
        public Double getUsage() { return usage; }
        public void setUsage(Double usage) { this.usage = usage; }
        
        public String getFileName() { return fileName; }
        public void setFileName(String fileName) { this.fileName = fileName; }
        
        @Override
        public String toString() {
            return "CdrMessage{" +
                   "source='" + source + '\'' +
                   ", destination='" + destination + '\'' +
                   ", starttime='" + starttime + '\'' +
                   ", service='" + service + '\'' +
                   ", usage=" + usage +
                   ", fileName='" + fileName + '\'' +
                   '}';
        }
    }
}