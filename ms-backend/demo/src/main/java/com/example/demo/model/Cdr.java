package com.example.demo.model;
import java.time.LocalDateTime;
import java.util.Objects;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Enumerated;
import jakarta.persistence.EnumType;

@Entity
public class Cdr {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String source;
    private String destination;
    private LocalDateTime startTime;

    @Enumerated(EnumType.STRING)
    private ServiceType serviceType;

    @Column(name = "`usage`")
    private double usage;

    private String fileName;


    public Cdr() {}

    public Cdr(String source, String destination, LocalDateTime startTime,
               ServiceType serviceType, double usage, String fileName) {
        this.source = source;
        this.destination = destination;
        this.startTime = startTime;
        this.serviceType = serviceType;
        this.usage = usage;
        this.fileName = fileName;
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getSource() { return source; }
    public void setSource(String source) { this.source = source; }

    public String getDestination() { return destination; }
    public void setDestination(String destination) { this.destination = destination; }

    public LocalDateTime getStartTime() { return startTime; }
    public void setStartTime(LocalDateTime startTime) { this.startTime = startTime; }

    public ServiceType getServiceType() { return serviceType; }
    public void setServiceType(ServiceType serviceType) { this.serviceType = serviceType; }

    public Double getUsage() { return usage; }
    public void setUsage(Double usage) { this.usage = usage; }

    public String getFileName() { return fileName; }
    public void setFileName(String fileName) { this.fileName = fileName; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Cdr cdr = (Cdr) o;
        return Objects.equals(id, cdr.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    public enum ServiceType {
        VOICE,
        SMS,
        DATA
    }

}
