package com.example.demo.model;

public class ServiceTypeUsage {
    private String serviceType;
    private double totalUsage;
    private long callCount;
    
    public ServiceTypeUsage() {
    }
    
    public ServiceTypeUsage(String serviceType, double totalUsage, long callCount) {
        this.serviceType = serviceType;
        this.totalUsage = totalUsage;
        this.callCount = callCount;
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