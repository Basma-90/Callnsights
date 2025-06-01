package com.example.demo.service;
import com.example.demo.model.Cdr;
import com.example.demo.repository.CdrRepository;
import org.springframework.stereotype.Service;
import java.util.List;
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
}
