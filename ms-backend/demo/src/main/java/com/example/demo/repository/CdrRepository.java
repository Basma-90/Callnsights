package com.example.demo.repository;
import java.util.List;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import com.example.demo.model.Cdr;

@Repository
public interface CdrRepository extends JpaRepository<Cdr, Long> {
    List<Cdr> findBySource(String source);
}
