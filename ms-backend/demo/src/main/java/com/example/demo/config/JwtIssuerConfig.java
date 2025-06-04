package com.example.demo.config;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.oauth2.core.DelegatingOAuth2TokenValidator;
import org.springframework.security.oauth2.core.OAuth2Error;
import org.springframework.security.oauth2.core.OAuth2TokenValidator;
import org.springframework.security.oauth2.core.OAuth2TokenValidatorResult;
import org.springframework.security.oauth2.jwt.*;

@Configuration
public class JwtIssuerConfig {
    private static final Logger logger = LoggerFactory.getLogger(JwtIssuerConfig.class);

    @Value("${keycloak.auth-server-url:http://localhost:8081}")
    private String keycloakUrl;
    
    @Value("${keycloak.realm:cdr-platform}")
    private String realm;
    
    @Value("${allowed.token.issuers:http://localhost:5173/realms/cdr-platform,http://localhost:8081/realms/cdr-platform}")
    private String allowedIssuers;

    @Bean
    public JwtDecoder jwtDecoder() {
        String jwkSetUri = keycloakUrl + "/realms/" + realm + "/protocol/openid-connect/certs";
        logger.info("Configuring JWT decoder with JWK Set URI: {}", jwkSetUri);
        
        NimbusJwtDecoder jwtDecoder = NimbusJwtDecoder.withJwkSetUri(jwkSetUri).build();
        
        OAuth2TokenValidator<Jwt> defaultValidator = JwtValidators.createDefault();
        
        String[] issuers = allowedIssuers.split(",");
        CustomIssuerValidator customIssuerValidator = new CustomIssuerValidator(issuers);
        
        OAuth2TokenValidator<Jwt> validator = new DelegatingOAuth2TokenValidator<>(
            defaultValidator, customIssuerValidator);
        
        jwtDecoder.setJwtValidator(validator);
        
        return jwtDecoder;
    }
    
    private static class CustomIssuerValidator implements OAuth2TokenValidator<Jwt> {
        private static final Logger logger = LoggerFactory.getLogger(CustomIssuerValidator.class);
        private final String[] allowedIssuers;
        
        public CustomIssuerValidator(String[] allowedIssuers) {
            this.allowedIssuers = allowedIssuers;
        }

        @Override
        public OAuth2TokenValidatorResult validate(Jwt jwt) {
            String tokenIssuer = jwt.getIssuer().toString();
            logger.debug("Validating token with issuer: {}", tokenIssuer);
            
            for (String allowedIssuer : allowedIssuers) {
                if (tokenIssuer.equals(allowedIssuer.trim())) {
                    logger.debug("Issuer {} is valid", tokenIssuer);
                    return OAuth2TokenValidatorResult.success();
                }
            }
            
            logger.warn("Invalid issuer: {}", tokenIssuer);
            OAuth2Error error = new OAuth2Error("invalid_issuer", 
                "The iss claim is not valid. Expected one of: " + String.join(", ", allowedIssuers), 
                null);
            return OAuth2TokenValidatorResult.failure(error);
        }
    }
}