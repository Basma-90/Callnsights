package com.example.demo.model;

public class DestinationUsage {
    private String destination;
    private double totalUsage;
    private long callCount;
    private String serviceType; 

    
    public DestinationUsage() {
    }
    
    public DestinationUsage(String destination, double totalUsage, long callCount, String serviceType) {
        this.destination = destination;
        this.serviceType = serviceType;
         this.totalUsage = totalUsage;
        this.callCount = callCount;
    }

    public String getDestination() {
        return destination;
    }

    public void setDestination(String destination) {
        this.destination = destination;
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

    public String getServiceType() {
        return serviceType;
    }

   public void setServiceType(String serviceType){
        this.serviceType = serviceType;
   }
}