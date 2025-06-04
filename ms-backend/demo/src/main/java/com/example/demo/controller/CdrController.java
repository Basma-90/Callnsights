package com.example.demo.controller;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import com.example.demo.model.Cdr;
import com.example.demo.service.CdrService;
import com.example.demo.model.ServiceTypeUsage;
import com.example.demo.model.SourceUsage;
import com.example.demo.model.DestinationUsage;

@RestController
@RequestMapping("/api/cdrs")
public class CdrController {

    @Autowired
    private CdrService service;

    @GetMapping
    public List<Cdr> getCdrs() {
        return service.getAllCdrs();
    }

    @GetMapping("/{id}")
    public ResponseEntity<Cdr> getCdrById(@PathVariable Long id) {
        Cdr cdr = service.getCdrById(id);
        if (cdr != null) {
            return ResponseEntity.ok(cdr);
        } else {
            return ResponseEntity.notFound().build();
        }
    }

    @PostMapping
    public ResponseEntity<Cdr> createCdr(@RequestBody Cdr cdr) {
        service.saveCdr(cdr);
        return ResponseEntity.ok(cdr);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteCdr(@PathVariable Long id) {
        service.deleteCdr(id);
        return ResponseEntity.noContent().build();
    }

    @PostMapping("/update")
    public ResponseEntity<Cdr> updateCdr(@RequestBody Cdr cdr) {
        try {
            service.updateCdr(cdr);
            return ResponseEntity.ok(cdr);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(null);
        }
    }

    @GetMapping("/source")
    public ResponseEntity<List<Cdr>> getCdrsBySource(@RequestParam String source) {
        List<Cdr> cdrs = service.getCdrsBySource(source);
        if (cdrs.isEmpty()) {
            return ResponseEntity.notFound().build();
        } else {
            return ResponseEntity.ok(cdrs);
        }
    }

    @GetMapping("/service-type")
    public ResponseEntity<List<Cdr>> getCdrsByServiceType(@RequestParam String serviceType) {
        List<Cdr> cdrs = service.getCdrsByServiceType(serviceType);
        if (cdrs.isEmpty()) {
            return ResponseEntity.notFound().build();
        } else {
            return ResponseEntity.ok(cdrs);
        }
    }

    @GetMapping("/usage-range")
    public ResponseEntity<List<Cdr>> getCdrsByUsageRange(@RequestParam Double minUsage, @RequestParam Double maxUsage) {
        List<Cdr> cdrs = service.getCdrsByUsageRange(minUsage, maxUsage);
        if (cdrs.isEmpty()) {
            return ResponseEntity.notFound().build();
        } else {
            return ResponseEntity.ok(cdrs);
        }
    }

    @GetMapping("/aggregated")
public ResponseEntity<?> getAggregatedCdrs(
        @RequestParam(required = false, defaultValue = "day") String groupBy,
        @RequestParam(required = false) String serviceType,
        @RequestParam(required = false) String startDate,
        @RequestParam(required = false) String endDate) {
    
    try {
        switch (groupBy.toLowerCase()) {
            case "day":
                List<ReportData> dailyData = service.getAggregatedCdrsByDay(serviceType, startDate, endDate);
                return ResponseEntity.ok(dailyData);
            case "service":
                List<ServiceTypeUsage> serviceData = service.getAggregatedCdrsByServiceType(startDate, endDate);
                return ResponseEntity.ok(serviceData);
            case "source":
                List<SourceUsage> sourceData = service.getAggregatedCdrsBySource(startDate, endDate);
                return ResponseEntity.ok(sourceData);
            case "destination":
                List<DestinationUsage> destData = service.getAggregatedCdrsByDestination(startDate, endDate);
                return ResponseEntity.ok(destData);
            default:
                return ResponseEntity.badRequest().body("Invalid groupBy parameter. Supported values: day, service, source, destination");
        }
    } catch (Exception e) {
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                .body("Error processing aggregation request: " + e.getMessage());
    }
}

    @GetMapping("/health")
    public ResponseEntity<String> healthCheck() {
        return ResponseEntity.ok("Cdr Service is running");
    }
}