# Synthetic Data Patterns for ChatBI Demos

## Why Synthetic Data

- Real customer data is sensitive and can't be used in demos.
- Synthetic data must look realistic to be convincing.
- Mexican business context (MXN, RFC, states, company names) makes demos relatable for LATAM audiences.

## Data Generation Principles

1. **Reproducibility**: Use fixed random seeds for consistent demo data.
2. **Realism**: Mexican company names, realistic amounts (MXN), proper RFC format.
3. **Distribution**: Follow real-world distributions (most vendors are low-risk, few are critical).
4. **Relationships**: Foreign keys must match (vendors exist in both dim_vendor and fact_transaction).
5. **Edge cases**: Include some outliers (very high amounts, very low scores) for interesting queries.

## Domain Templates

### Financial Services (Risk Analysis)

```python
VENDOR_NAMES = [
    "Transportes del Valle", "Suministros Industriales SA",
    "Constructora del Bajío", "Servicios Tecnológicos MX",
    "Distribuidora Nacional", "Grupo Logístico Centro",
    "Importaciones del Pacífico", "Manufacturas del Norte",
]

RISK_DISTRIBUTION = {"BAJO": 0.30, "MEDIO": 0.35, "ALTO": 0.25, "CRITICO": 0.10}

AMOUNT_RANGES = {
    "BAJO": (50_000, 500_000),
    "MEDIO": (500_000, 2_000_000),
    "ALTO": (2_000_000, 8_000_000),
    "CRITICO": (8_000_000, 25_000_000),
}
```

### Retail / E-commerce

```python
PRODUCT_CATEGORIES = [
    "Electrónicos", "Ropa", "Hogar", "Deportes",
    "Alimentos", "Salud", "Automotriz", "Oficina",
]

REGIONS = [
    "CDMX", "Jalisco", "Nuevo León", "Estado de México",
    "Puebla", "Guerrero", "Veracruz", "Yucatán",
]
```

### Healthcare

```python
HOSPITAL_TYPES = ["General", "Especializado", "Urgencias", "Laboratorio"]
PROCEDURE_CATEGORIES = ["Cirugía", "Diagnóstico", "Terapia", "Prevención"]
```

## Mexican Business Context

- **RFC format**: 3-4 letters + 6 digits + 3 characters (e.g., `TDE850101XYZ`)
- **Currency**: MXN (always specify, never use USD in LATAM demos)
- **States**: 32 Mexican states (CDMX, Jalisco, Nuevo León, etc.)
- **Company suffixes**: SA de CV, SAPI de CV, SC, AC
- **Amounts**: Realistic ranges (small vendors: $100K-$500K MXN, large: $5M-$50M MXN)
