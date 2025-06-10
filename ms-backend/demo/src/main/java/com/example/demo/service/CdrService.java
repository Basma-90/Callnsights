package com.example.demo.service;
import com.example.demo.controller.ReportData;
import com.example.demo.model.Cdr;
import com.example.demo.model.DestinationUsage;
import com.example.demo.model.ServiceTypeUsage;
import com.example.demo.model.SourceUsage;
import com.example.demo.repository.CdrRepository;
import org.springframework.stereotype.Service;

import java.util.Comparator;
import java.util.DoubleSummaryStatistics;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class CdrService {
    
    private final CdrRepository cdrRepository;

    public CdrService(CdrRepository cdrRepository) {
        this.cdrRepository = cdrRepository;
    }

    public Cdr saveCdr(Cdr cdr) {
        return cdrRepository.save(cdr);
    }

    public Cdr getCdrById(Long id) {
        return cdrRepository.findById(id).orElse(null);
    }

    public List<Cdr> getCdrsBySource(String source) {
        return cdrRepository.findBySource(source);
    }

    public List<Cdr> getAllCdrs() {
        return cdrRepository.findAll();
    }

    public void deleteCdr(Long id) {
        cdrRepository.deleteById(id);
    }

    public void updateCdr(Cdr cdr) {
        if (cdr.getId() != null && cdrRepository.existsById(cdr.getId())) {
            cdrRepository.save(cdr);
        } else {
            throw new IllegalArgumentException("CDR with id " + cdr.getId() + " does not exist.");
        }
    }

    public List<Cdr> getCdrsByServiceType(String serviceType) {
        return cdrRepository.findAll().stream()
                .filter(cdr -> cdr.getServiceType() != null &&
                               cdr.getServiceType().name().equalsIgnoreCase(serviceType))
                .collect(Collectors.toList());
    }

    public List<Cdr> getCdrsByUsageRange(Double minUsage, Double maxUsage) {
        return cdrRepository.findAll().stream()
                .filter(cdr -> cdr.getUsage() != null &&
                               cdr.getUsage() >= minUsage &&
                               cdr.getUsage() <= maxUsage)
                .collect(Collectors.toList());
    }

    private String getUsageUnit(String serviceType) {
        switch (serviceType.toUpperCase()) {
            case "VOICE": return "minutes";
            case "DATA": return "MB";
            case "SMS": return "messages";
            default: return "units";
        }
    }

    private double formatUsageForService(double usage, String serviceType) {
        switch (serviceType.toUpperCase()) {
            case "VOICE":
                return Math.round(usage * 100.0) / 100.0; 
            case "DATA":
                return Math.round(usage * 100.0) / 100.0; 
            case "SMS":
                return Math.round(usage); 
            default:
                return usage;
        }
    }

    public List<DestinationUsage> getAggregatedCdrsByDestination(String startDate, String endDate) {
        Map<String, Map<String, DoubleSummaryStatistics>> destServiceStats = cdrRepository.findAll().stream()
            .filter(cdr -> cdr.getDestination() != null &&
                          cdr.getStartTime() != null &&
                          cdr.getServiceType() != null)
            .filter(cdr -> startDate == null || 
                          cdr.getStartTime().toLocalDate().toString().compareTo(startDate) >= 0)
            .filter(cdr -> endDate == null || 
                          cdr.getStartTime().toLocalDate().toString().compareTo(endDate) <= 0)
            .collect(Collectors.groupingBy(
                    Cdr::getDestination,
                    Collectors.groupingBy(
                        cdr -> cdr.getServiceType().name(),
                        Collectors.summarizingDouble(Cdr::getUsage)
                    )
            ));

        return destServiceStats.entrySet().stream()
            .flatMap(destEntry -> {
                String destination = destEntry.getKey();
                Map<String, DoubleSummaryStatistics> serviceStats = destEntry.getValue();
                return serviceStats.entrySet().stream().map(serviceEntry -> {
                    String serviceType = serviceEntry.getKey();
                    DoubleSummaryStatistics stats = serviceEntry.getValue();

                    double totalUsage = formatUsageForService(stats.getSum(), serviceType);
                    long interactionCount = stats.getCount();

                    return new DestinationUsage(
                            destination,
                            totalUsage,
                            interactionCount,
                            serviceType
                    );
                });
            })
            .sorted(Comparator.comparing(DestinationUsage::getTotalUsage).reversed())
            .collect(Collectors.toList());
    }

    public List<SourceUsage> getAggregatedCdrsBySource(String startDate, String endDate) {
        Map<String, Map<String, DoubleSummaryStatistics>> sourceServiceStats = cdrRepository.findAll().stream()
            .filter(cdr -> cdr.getSource() != null &&
                          cdr.getStartTime() != null &&
                          cdr.getServiceType() != null)
            .filter(cdr -> startDate == null || 
                          cdr.getStartTime().toLocalDate().toString().compareTo(startDate) >= 0)
            .filter(cdr -> endDate == null || 
                          cdr.getStartTime().toLocalDate().toString().compareTo(endDate) <= 0)
            .collect(Collectors.groupingBy(
                    Cdr::getSource,
                    Collectors.groupingBy(
                        cdr -> cdr.getServiceType().name(),
                        Collectors.summarizingDouble(Cdr::getUsage)
                    )
            ));

        return sourceServiceStats.entrySet().stream()
            .flatMap(sourceEntry -> {
                String source = sourceEntry.getKey();
                Map<String, DoubleSummaryStatistics> serviceStats = sourceEntry.getValue();

                return serviceStats.entrySet().stream().map(serviceEntry -> {
                    String serviceType = serviceEntry.getKey();
                    DoubleSummaryStatistics stats = serviceEntry.getValue();

                    double totalUsage = formatUsageForService(stats.getSum(), serviceType);
                    long interactionCount = stats.getCount();

                    return new SourceUsage(
                            source,
                            totalUsage,
                            interactionCount,
                            serviceType
                    );
                });
            })
            .sorted(Comparator.comparing(SourceUsage::getTotalUsage).reversed())
            .collect(Collectors.toList());
    }

    public List<ServiceTypeUsage> getAggregatedCdrsByServiceType(String startDate, String endDate) {
        return cdrRepository.findAll().stream()
            .filter(cdr -> cdr.getServiceType() != null &&
                          cdr.getStartTime() != null)
            .filter(cdr -> startDate == null || 
                          cdr.getStartTime().toLocalDate().toString().compareTo(startDate) >= 0)
            .filter(cdr -> endDate == null || 
                          cdr.getStartTime().toLocalDate().toString().compareTo(endDate) <= 0)
            .collect(Collectors.groupingBy(
                    cdr -> cdr.getServiceType().name(),
                    Collectors.summarizingDouble(Cdr::getUsage)
            ))
            .entrySet().stream()
            .map(entry -> {
                String serviceType = entry.getKey();
                double totalUsage = formatUsageForService(entry.getValue().getSum(), serviceType);

                return new ServiceTypeUsage(
                        serviceType,
                        totalUsage,
                        entry.getValue().getCount()
                );
            })
            .collect(Collectors.toList());
    }
    public List<ReportData> getAggregatedCdrsByDay(String serviceType, String startDate, String endDate) {
    Map<String, Map<String, DoubleSummaryStatistics>> groupedByDayAndService = cdrRepository.findAll().stream()
        .filter(cdr -> cdr.getStartTime() != null) 
        .filter(cdr -> serviceType == null || 
                      (cdr.getServiceType() != null && 
                       cdr.getServiceType().name().equalsIgnoreCase(serviceType))) 
        .filter(cdr -> startDate == null || 
                      cdr.getStartTime().toLocalDate().toString().compareTo(startDate) >= 0) 
        .filter(cdr -> endDate == null || 
                      cdr.getStartTime().toLocalDate().toString().compareTo(endDate) <= 0) 
        .collect(Collectors.groupingBy(
            cdr -> cdr.getStartTime().toLocalDate().toString(), 
            Collectors.groupingBy(
                cdr -> cdr.getServiceType().name(),
                Collectors.summarizingDouble(Cdr::getUsage) 
            )
        ));

    return groupedByDayAndService.entrySet().stream()
        .flatMap(dayEntry -> {
            String date = dayEntry.getKey();
            Map<String, DoubleSummaryStatistics> serviceStats = dayEntry.getValue();

            return serviceStats.entrySet().stream().map(serviceEntry -> {
                String serviceTypeKey = serviceEntry.getKey();
                DoubleSummaryStatistics stats = serviceEntry.getValue();
                double totalUsage = stats.getSum();
                long interactionCount = stats.getCount();

                String usageUnit = getUsageUnit(serviceTypeKey);
                totalUsage = formatUsageForService(totalUsage, serviceTypeKey);

                return new ReportData(
                    date,
                    totalUsage,
                    interactionCount,
                    serviceTypeKey,
                    usageUnit
                );
            });
        })
        .sorted(Comparator.comparing(ReportData::getDate)) // Sort by date
        .collect(Collectors.toList());
}
}