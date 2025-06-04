package com.example.demo.controller;

import java.time.LocalDate;

public class ReportData {
    private String date;
    private double totalUsage;
    private long callCount;
    
    public ReportData() {
    }
    
    public ReportData(String date, double totalUsage, long callCount) {
        this.date = date;
        this.totalUsage = totalUsage;
        this.callCount = callCount;
    }
    
    public ReportData(LocalDate date, double totalUsage, long callCount) {
        this.date = date.toString();
        this.totalUsage = totalUsage;
        this.callCount = callCount;
    }

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

    public long getCallCount() {
        return callCount;
    }

    public void setCallCount(long callCount) {
        this.callCount = callCount;
    }

    @Override
    public String toString() {
        return "ReportData{" +
                "date='" + date + '\'' +
                ", totalUsage=" + totalUsage +
                ", callCount=" + callCount +
                '}';
    }
}