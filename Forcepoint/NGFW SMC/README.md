# Forcepoint NGFW Assets
Assets for the Itential Platform.

## OpenAPIs
- [SMC API 7.0](./OpenAPIs/smc_api_7.0.json)

> **⚠️ Integration Model limitation:** The SMC API uses session-cookie authentication
> (`POST /7.0/login` → `Set-Cookie: JSESSIONID`). Itential Integration Models cannot
> perform this auth flow declaratively until
> [IPSO-9866](https://itential.atlassian.net/browse/IPSO-9866) is resolved.
> The spec is included for reference and future use.

#### Dependencies
- Forcepoint NGFW SMC 7.0 instance
- SMC API Client element configured in the SMC Management Client (generates the `authenticationkey`)
- [Forcepoint SMC API 7.0 Documentation](https://help.forcepoint.com/ngfw/en-us/7.0.0/smc_api_ug/)
