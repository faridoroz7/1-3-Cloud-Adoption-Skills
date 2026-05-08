#!/usr/bin/env python3
"""Generate synthetic data for ChatBI demos.

Creates realistic datasets with Mexican business context:
- Vendors with risk scores and financial data
- Customers with KYC levels and limits
- Transactions with anomaly detection patterns
- Contract risk analysis results

Output: SQL seed files + JSON for direct loading.

Usage:
    python3 scripts/generate-chatbi-demo-data.py [--domain financial|retail|healthcare] [--count N]
"""

import json
import random
import argparse
from datetime import datetime, timedelta

# ─── Mexican Business Context ────────────────────────────

VENDOR_NAMES = [
    "Transportes del Valle SA de CV", "Suministros Industriales MX SA de CV",
    "Constructora del Bajío SAPI de CV", "Servicios Tecnológicos del Norte SA de CV",
    "Distribuidora Nacional SC", "Grupo Logístico Centro SA de CV",
    "Importaciones del Pacífico SA de CV", "Manufacturas del Bajío SA de CV",
    "Comercializadora del Sureste SC", "Alimentos Frescos MX SA de CV",
    "Energías Renovables del Norte SA de CV", "Consultoría Fiscal Centro SC",
    "Seguros y Fianzas del Bajío SA de CV", "Minera del Sureste SA de CV",
    "Agrícola del Valle de México SA de CV", "Químicos Industriales MX SC",
    "Telecomunicaciones del Pacífico SA de CV", "Turismo y Hospitalidad SA de CV",
    "Metalúrgica del Norte SA de CV", "Farmacéutica Nacional SA de CV",
]

CUSTOMER_NAMES = [
    "Grupo Salinas SA de CV", "FEMSA SA de CV", "Banorte SA de CV",
    "Bimbo SA de CV", "Cemex SA de CV", "América Móvil SA de CV",
    "Walmex SA de CV", "Liverpool SA de CV", "Palacio de Hierro SA de CV",
    "Televisa SA de CV", "GAP SA de CV", "Vitro SA de CV",
    "Alfa SA de CV", "IUSA SA de CV", "Condumex SA de CV",
]

MEXICAN_STATES = [
    "Ciudad de México", "Jalisco", "Nuevo León", "Estado de México",
    "Puebla", "Guanajuato", "Querétaro", "Veracruz", "Yucatán",
    "Chihuahua", "Sonora", "Coahuila", "Michoacán", "Guerrero",
]

CITIES = {
    "Ciudad de México": ["CDMX", "Ecatepec", "Nezahualcóyotl"],
    "Jalisco": ["Guadalajara", "Zapopan", "Tlaquepaque"],
    "Nuevo León": ["Monterrey", "San Nicolás", "Guadalupe"],
    "Estado de México": ["Toluca", "Naucalpan", "Tultitlán"],
    "Puebla": ["Puebla", "Tehuacán", "Atlixco"],
}

SECTORS = ["Tecnología", "Manufactura", "Servicios", "Comercio", "Construcción", "Salud", "Finanzas"]

ANOMALY_TYPES = ["Ninguna", "Monto inusual", "Frecuencia alta", "Ubicación sospechosa", "Duplicado"]

RISK_LEVELS = ["BAJO", "MEDIO", "ALTO", "CRITICO"]

CONTRACT_TYPES = [
    "Suministro de equipos", "Servicios de consultoría", "Contrato de mantenimiento",
    "Licenciamiento de software", "Servicios de nube", "Contrato de transporte",
    "Servicios profesionales", "Construcción de infraestructura",
]


def generate_vendors(count=50, seed=42):
    """Generate vendor master data."""
    random.seed(seed)
    vendors = []

    for i in range(count):
        name = random.choice(VENDOR_NAMES) + f" #{i+1:03d}"
        state = random.choice(MEXICAN_STATES)
        city = random.choice(CITIES.get(state, ["Capital"]))
        sector = random.choice(SECTORS)

        # Risk distribution: 30% BAJO, 35% MEDIO, 25% ALTO, 10% CRITICO
        risk_level = random.choices(
            RISK_LEVELS, weights=[0.30, 0.35, 0.25, 0.10], k=1
        )[0]

        risk_score = {
            "BAJO": random.uniform(0, 3),
            "MEDIO": random.uniform(4, 6),
            "ALTO": random.uniform(7, 8),
            "CRITICO": random.uniform(9, 10),
        }[risk_level]

        annual_revenue = random.randint(1_000_000, 100_000_000)
        debt_ratio = round(random.uniform(0.1, 0.8), 2)
        contract_count = random.randint(1, 20)
        employee_count = random.randint(10, 500)

        rfc = f"{name[:3].upper()}{random.randint(10,99)}{random.randint(1000,9999)}{random.choice('ABCDEF0-9')}{random.choice('ABCDEF0-9')}{random.choice('ABCDEF0-9')}"

        vendors.append({
            "vendor_id": f"VND-{i+1:04d}",
            "name": name,
            "rfc": rfc,
            "sector": sector,
            "state": state,
            "city": city,
            "risk_level": risk_level,
            "risk_score": round(risk_score, 1),
            "annual_revenue_mxn": annual_revenue,
            "debt_ratio": debt_ratio,
            "contract_count": contract_count,
            "employee_count": employee_count,
        })

    return vendors


def generate_customers(count=30, seed=42):
    """Generate customer master data."""
    random.seed(seed + 1)
    customers = []

    for i in range(count):
        name = random.choice(CUSTOMER_NAMES) + f" #{i+1:03d}"
        state = random.choice(MEXICAN_STATES)
        city = random.choice(CITIES.get(state, ["Capital"]))
        kyc_level = random.choices(["Básico", "Medio", "Avanzado"], weights=[0.3, 0.5, 0.2], k=1)[0]

        monthly_limit = {
            "Básico": random.randint(100_000, 500_000),
            "Medio": random.randint(500_000, 2_000_000),
            "Avanzado": random.randint(2_000_000, 10_000_000),
        }[kyc_level]

        customers.append({
            "customer_id": f"CUST-{i+1:04d}",
            "name": name,
            "kyc_level": kyc_level,
            "monthly_limit_mxn": monthly_limit,
            "risk_score": round(random.uniform(0, 8), 1),
            "city": city,
            "state": state,
            "account_age_days": random.randint(30, 3650),
        })

    return customers


def generate_transactions(vendors, customers, count=500, seed=42):
    """Generate transaction data with anomaly patterns."""
    random.seed(seed + 2)
    transactions = []

    for i in range(count):
        vendor = random.choice(vendors)
        customer = random.choice(customers)

        # Amount correlates with vendor revenue
        base_amount = vendor["annual_revenue_mxn"] / 12
        amount = round(random.uniform(0.1, 3.0) * base_amount, 2)

        # 8% anomaly rate
        anomaly_type = random.choices(
            ANOMALY_TYPES, weights=[0.85, 0.05, 0.04, 0.03, 0.03], k=1
        )[0]

        tx_date = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 450))

        transactions.append({
            "tx_id": f"TX-{i+1:06d}",
            "vendor_id": vendor["vendor_id"],
            "customer_id": customer["customer_id"],
            "amount_mxn": amount,
            "anomaly_type": anomaly_type,
            "timestamp": tx_date.strftime("%Y-%m-%d %H:%M:%S"),
            "city_from": vendor["city"],
            "city_to": customer["city"],
        })

    return transactions


def generate_risk_results(vendors, count=20, seed=42):
    """Generate contract risk analysis results."""
    random.seed(seed + 3)
    results = []

    alert_pools = {
        "BAJO": ["Sin anomalías detectadas", "Términos estándar"],
        "MEDIO": ["Monto requiere revisión", "Cláusula ambigua"],
        "ALTO": ["Garantía insuficiente", "Penalización fuera de rango"],
        "CRITICO": ["Sin garantías", "Exención total de responsabilidad"],
    }

    for i in range(count):
        vendor = random.choice(vendors)
        risk_level = vendor["risk_level"]
        score = vendor["risk_score"]
        amount = random.randint(100_000, 15_000_000)
        contract_type = random.choice(CONTRACT_TYPES)

        alerts = random.sample(alert_pools[risk_level], k=min(2, len(alert_pools[risk_level])))

        results.append({
            "contract_number": f"CTR-{random.randint(1000, 9999)}",
            "vendor_name": vendor["name"],
            "monto_total": amount,
            "plazo_dias": random.choice([30, 60, 90, 180, 365]),
            "penalizacion_pct": round(random.uniform(0, 15), 1),
            "garantia_pct": round(random.uniform(0, 30), 1),
            "risk_score": round(score, 1),
            "risk_level": risk_level,
            "alertas": json.dumps(alerts, ensure_ascii=False),
            "recomendaciones": json.dumps([f"Revisión de {contract_type.lower()}"], ensure_ascii=False),
            "resumen": f"Análisis de {contract_type.lower()}: {len(alerts)} alertas.",
            "llm_provider": "synthetic-demo",
            "analyzed_at": (datetime.now() - timedelta(days=random.randint(0, 30))).strftime("%Y-%m-%d %H:%M:%S"),
        })

    return results


def to_sql(table_name, records, schema="public"):
    """Convert records to INSERT SQL statements."""
    if not records:
        return ""

    columns = list(records[0].keys())
    lines = [f"-- Synthetic data for {schema}.{table_name}"]
    lines.append(f"TRUNCATE TABLE {schema}.{table_name};")

    for record in records:
        values = []
        for col in columns:
            val = record[col]
            if val is None:
                values.append("NULL")
            elif isinstance(val, (int, float)):
                values.append(str(val))
            elif isinstance(val, str):
                escaped = val.replace("'", "''")
                values.append(f"'{escaped}'")
            else:
                values.append(f"'{str(val)}'")
        lines.append(
            f"INSERT INTO {schema}.{table_name} ({', '.join(columns)}) VALUES ({', '.join(values)});"
        )

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate synthetic ChatBI demo data")
    parser.add_argument("--domain", choices=["financial", "retail", "healthcare"], default="financial")
    parser.add_argument("--count", type=int, default=50, help="Number of vendors/customers")
    parser.add_argument("--output-dir", type=str, default=".")
    args = parser.parse_args()

    vendors = generate_vendors(args.count)
    customers = generate_customers(args.count // 2)
    transactions = generate_transactions(vendors, customers, args.count * 10)
    risk_results = generate_risk_results(vendors, args.count // 3)

    # Write SQL seed file
    sql_path = f"{args.output_dir}/chatbi-demo-seed.sql"
    with open(sql_path, "w", encoding="utf-8") as f:
        f.write("-- ChatBI Demo Data\n")
        f.write("-- Generated by generate-chatbi-demo-data.py\n")
        f.write("-- Domain: {}\n\n".format(args.domain))
        f.write(to_sql("vendors", vendors) + "\n\n")
        f.write(to_sql("customers", customers) + "\n\n")
        f.write(to_sql("transactions", transactions) + "\n\n")
        f.write(to_sql("risk_results", risk_results) + "\n")

    # Write JSON for API loading
    json_path = f"{args.output_dir}/chatbi-demo-data.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump({
            "vendors": vendors,
            "customers": customers,
            "transactions": transactions,
            "risk_results": risk_results,
        }, f, ensure_ascii=False, indent=2)

    print(f"Generated synthetic data:")
    print(f"  Vendors:        {len(vendors)}")
    print(f"  Customers:      {len(customers)}")
    print(f"  Transactions:   {len(transactions)}")
    print(f"  Risk results:   {len(risk_results)}")
    print(f"  SQL seed:       {sql_path}")
    print(f"  JSON data:      {json_path}")


if __name__ == "__main__":
    main()
