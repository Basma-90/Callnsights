package com.example.demo.controller;

public class ReportData {
    private String date;
    private double totalUsage;
    private long interactionCount;
    private String serviceType; // New field for service type
    private String usageUnit;   // Optional: Unit of usage (e.g., minutes, messages, MB)

    public ReportData(String date, double totalUsage, long interactionCount, String serviceType, String usageUnit) {
        this.date = date;
        this.totalUsage = totalUsage;
        this.interactionCount = interactionCount;
        this.serviceType = serviceType;
        this.usageUnit = usageUnit;
    }

    // Getters and setters
    public String getDate() {
        return date;
    }

    public void setDate(String date) {
        this.date = date;
    }

    public double getTotalUsage() {
        return totalUsage;
    }

    public void setTotalUsage(double totalUsage) {
        this.totalUsage = totalUsage;
    }

    public long getInteractionCount() {
        return interactionCount;
    }

    public void setInteractionCount(long interactionCount) {
        this.interactionCount = interactionCount;
    }

    public String getServiceType() {
        return serviceType;
    }

    public void setServiceType(String serviceType) {
        this.serviceType = serviceType;
    }

    public String getUsageUnit() {
        return usageUnit;
    }

    public void setUsageUnit(String usageUnit) {
        this.usageUnit = usageUnit;
    }
}