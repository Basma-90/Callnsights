package com.example.demo;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import java.util.Map;

@RestController
@RequestMapping("/api/v1")
public class HomeController {

@GetMapping("/home")
public Map<String, Object> home(@AuthenticationPrincipal Jwt jwt) {
    if (jwt == null) {
        return Map.of("message", "Unauthorized");
    }
    return Map.of(
        "message", "Welcome to CDR Backend!",
        "username", jwt.getClaimAsString("username"),
        "email", jwt.getClaimAsString("email")
    );
}
}