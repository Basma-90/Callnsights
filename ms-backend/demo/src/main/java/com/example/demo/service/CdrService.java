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

    public List<ReportData> getAggregatedCdrsByDay(String serviceType, String startDate, String endDate) {
        List<Cdr> filteredCdrs = cdrRepository.findAll().stream()
            .filter(cdr -> cdr.getStartTime() != null)
            .filter(cdr -> startDate == null || cdr.getStartTime().toLocalDate().toString().compareTo(startDate) >= 0)
            .filter(cdr -> endDate == null || cdr.getStartTime().toLocalDate().toString().compareTo(endDate) <= 0)
            .filter(cdr -> serviceType == null || 
                   (cdr.getServiceType() != null && 
                    cdr.getServiceType().name().equalsIgnoreCase(serviceType)))
            .collect(Collectors.toList());
    
    Map<String, DoubleSummaryStatistics> groupedByDay = filteredCdrs.stream()
            .collect(Collectors.groupingBy(
                cdr -> cdr.getStartTime().toLocalDate().toString(),
                Collectors.summarizingDouble(Cdr::getUsage)
            ));
    
    return groupedByDay.entrySet().stream()
            .map(entry -> new ReportData(
                    entry.getKey(),
                    entry.getValue().getSum(),
                    entry.getValue().getCount()
            ))
            .sorted(Comparator.comparing(ReportData::getDate))
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
            .map(entry -> new ServiceTypeUsage(
                    entry.getKey(),
                    entry.getValue().getSum(),
                    entry.getValue().getCount()
            ))
            .collect(Collectors.toList());
    }

    public List<SourceUsage> getAggregatedCdrsBySource(String startDate, String endDate) {
         return cdrRepository.findAll().stream()
            .filter(cdr -> cdr.getSource() != null &&
                          cdr.getStartTime() != null)
            .filter(cdr -> startDate == null || 
                          cdr.getStartTime().toLocalDate().toString().compareTo(startDate) >= 0)
            .filter(cdr -> endDate == null || 
                          cdr.getStartTime().toLocalDate().toString().compareTo(endDate) <= 0)
            .collect(Collectors.groupingBy(
                    Cdr::getSource,
                    Collectors.summarizingDouble(Cdr::getUsage)
            ))
            .entrySet().stream()
            .map(entry -> new SourceUsage(
                    entry.getKey(),
                    entry.getValue().getSum(),
                    entry.getValue().getCount()
            ))
            .collect(Collectors.toList());

    }

    public List<DestinationUsage> getAggregatedCdrsByDestination(String startDate, String endDate) {
       return cdrRepository.findAll().stream()
            .filter(cdr -> cdr.getDestination() != null &&
                          cdr.getStartTime() != null)
            // Filter by date range if specified
            .filter(cdr -> startDate == null || 
                          cdr.getStartTime().toLocalDate().toString().compareTo(startDate) >= 0)
            .filter(cdr -> endDate == null || 
                          cdr.getStartTime().toLocalDate().toString().compareTo(endDate) <= 0)
            // Group by destination
            .collect(Collectors.groupingBy(
                    Cdr::getDestination,
                    Collectors.summarizingDouble(Cdr::getUsage)
            ))
            .entrySet().stream()
            .map(entry -> new DestinationUsage(
                    entry.getKey(),
                    entry.getValue().getSum(),
                    entry.getValue().getCount()
            ))
            .collect(Collectors.toList());

    }
}
