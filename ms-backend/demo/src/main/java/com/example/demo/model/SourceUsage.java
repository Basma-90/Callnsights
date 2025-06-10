package com.example.demo.model;

public class SourceUsage {
    private String source;
    private double totalUsage;
    private long callCount;
    private String serviceType;
    
    public SourceUsage() {
    }
    
    public SourceUsage(String source, double totalUsage, long callCount, String serviceType) {
        this.source = source;
        this.totalUsage = totalUsage;
        this.callCount = callCount;
        this.serviceType= serviceType;
    }

    public String getSource() {
        return source;
    }

    public void setSource(String source) {
        this.source = source;
    }

    public String getServiceType() {
        return serviceType;
    }

    public void setServiceType(String serviceType) {
        this.serviceType = serviceType;
    }

    public double getTotalUsage() {
        return totalUsage;
    }

    public void setTotalUsage(double totalUsage) {
        this.totalUsage = totalUsage;
    }

    public long getCallCount() {
        return callCount;
    }

    public void setCallCount(long callCount) {
        this.callCount = callCount;
    }
}