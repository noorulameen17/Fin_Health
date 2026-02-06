from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Boolean, Enum as SQLEnum
from sqlalchemy.sql import func
from app.core.database import Base
import enum

class IndustryType(str, enum.Enum):
    MANUFACTURING = "Manufacturing"
    RETAIL = "Retail"
    AGRICULTURE = "Agriculture"
    SERVICES = "Services"
    LOGISTICS = "Logistics"
    ECOMMERCE = "E-commerce"
    HEALTHCARE = "Healthcare"
    TECHNOLOGY = "Technology"

class RiskLevel(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"

class ProductType(str, enum.Enum):
    WORKING_CAPITAL_LOAN = "Working Capital Loan"
    TERM_LOAN = "Term Loan"
    TRADE_CREDIT = "Trade Credit"
    EQUIPMENT_FINANCING = "Equipment Financing"
    INVOICE_FINANCING = "Invoice Financing"
    OVERDRAFT = "Overdraft Facility"
    LETTER_OF_CREDIT = "Letter of Credit"
    BANK_GUARANTEE = "Bank Guarantee"

class ComplianceType(str, enum.Enum):
    GST = "GST"
    TDS = "TDS"
    INCOME_TAX = "Income Tax"
    PF_ESI = "PF/ESI"
    COMPANIES_ACT = "Companies Act"

class ComplianceStatus(str, enum.Enum):
    COMPLIANT = "Compliant"
    PENDING = "Pending"
    OVERDUE = "Overdue"
    NON_COMPLIANT = "Non-Compliant"

class Company(Base):
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    registration_number = Column(String(100), unique=True)
    industry = Column(SQLEnum(IndustryType), nullable=False)
    email = Column(String(255))
    phone = Column(String(50))
    address = Column(Text)
    gstin = Column(String(15))  # GST Identification Number
    pan = Column(String(10))  # PAN Number (encrypted)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class FinancialDocument(Base):
    __tablename__ = "financial_documents"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    document_type = Column(String(50))  # balance_sheet, income_statement, cash_flow
    file_name = Column(String(255))
    file_path = Column(String(500))
    file_type = Column(String(10))  # csv, xlsx, pdf
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())
    processed = Column(Boolean, default=False)
    processed_at = Column(DateTime(timezone=True))
    data = Column(JSON)  # Parsed financial data

class FinancialMetrics(Base):
    __tablename__ = "financial_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    
    # Revenue & Profitability
    total_revenue = Column(Float)
    gross_profit = Column(Float)
    net_profit = Column(Float)
    operating_profit = Column(Float)
    ebitda = Column(Float)
    
    # Liquidity Ratios
    current_ratio = Column(Float)
    quick_ratio = Column(Float)
    cash_ratio = Column(Float)
    
    # Profitability Ratios
    gross_profit_margin = Column(Float)
    net_profit_margin = Column(Float)
    return_on_assets = Column(Float)
    return_on_equity = Column(Float)
    
    # Leverage Ratios
    debt_to_equity = Column(Float)
    debt_to_assets = Column(Float)
    interest_coverage = Column(Float)
    
    # Efficiency Ratios
    asset_turnover = Column(Float)
    inventory_turnover = Column(Float)
    receivables_turnover = Column(Float)
    
    # Cash Flow
    operating_cash_flow = Column(Float)
    investing_cash_flow = Column(Float)
    financing_cash_flow = Column(Float)
    free_cash_flow = Column(Float)
    
    # Working Capital
    working_capital = Column(Float)
    accounts_receivable = Column(Float)
    accounts_payable = Column(Float)
    inventory = Column(Float)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class CreditScore(Base):
    __tablename__ = "credit_scores"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    score = Column(Integer)  # 0-1000 scale
    rating = Column(String(5))  # AAA, AA, A, BBB, BB, B, C, D
    risk_level = Column(SQLEnum(RiskLevel))
    factors = Column(JSON)  # Breakdown of factors affecting score
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    
    # Overall Assessment
    financial_health_score = Column(Float)  # 0-100
    risk_level = Column(SQLEnum(RiskLevel))
    
    # AI Generated Insights
    strengths = Column(JSON)
    weaknesses = Column(JSON)
    opportunities = Column(JSON)
    threats = Column(JSON)
    
    # Recommendations
    cost_optimization = Column(JSON)
    revenue_enhancement = Column(JSON)
    working_capital_tips = Column(JSON)
    tax_optimization = Column(JSON)
    
    # Financial Product Recommendations
    recommended_products = Column(JSON)
    
    # Forecasts
    revenue_forecast = Column(JSON)
    cash_flow_forecast = Column(JSON)
    
    # Summary and Metadata
    executive_summary = Column(Text)
    language = Column(String(10), default="en")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class FinancialProduct(Base):
    __tablename__ = "financial_products"
    
    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(255), nullable=False)
    product_type = Column(SQLEnum(ProductType), nullable=False)
    provider_name = Column(String(255))  # Bank or NBFC name
    provider_type = Column(String(50))  # Bank / NBFC
    min_amount = Column(Float)
    max_amount = Column(Float)
    interest_rate_min = Column(Float)
    interest_rate_max = Column(Float)
    tenure_months_min = Column(Integer)
    tenure_months_max = Column(Integer)
    processing_fee_percentage = Column(Float)
    eligibility_criteria = Column(JSON)  # Min turnover, credit score, etc.
    features = Column(JSON)  # Key features and benefits
    documentation_required = Column(JSON)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class Forecast(Base):
    __tablename__ = "forecasts"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    forecast_type = Column(String(50))  # revenue, expenses, cash_flow, profit
    period_start = Column(DateTime(timezone=True))
    period_end = Column(DateTime(timezone=True))
    projected_values = Column(JSON)  # Monthly/quarterly projections
    scenarios = Column(JSON)  # Best case, worst case, likely
    confidence_level = Column(Float)
    methodology = Column(String(100))  # Linear, exponential, ML-based
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class IndustryBenchmark(Base):
    __tablename__ = "industry_benchmarks"
    
    id = Column(Integer, primary_key=True, index=True)
    industry = Column(SQLEnum(IndustryType), nullable=False)
    metric_name = Column(String(100))  # current_ratio, debt_to_equity, etc.
    percentile_25 = Column(Float)
    percentile_50 = Column(Float)  # Median
    percentile_75 = Column(Float)
    percentile_90 = Column(Float)
    sample_size = Column(Integer)
    year = Column(Integer)
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    
class TaxCompliance(Base):
    __tablename__ = "tax_compliance"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    compliance_type = Column(SQLEnum(ComplianceType), nullable=False)
    period = Column(String(20))  # FY2024-25, Q1-2024, etc.
    status = Column(SQLEnum(ComplianceStatus))
    due_date = Column(DateTime(timezone=True))
    completed_date = Column(DateTime(timezone=True))
    amount_payable = Column(Float)
    amount_paid = Column(Float)
    penalties = Column(Float, default=0)
    notes = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class GSTRecord(Base):
    __tablename__ = "gst_records"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    gstin = Column(String(15))
    return_period = Column(String(20))  # MM-YYYY
    return_type = Column(String(20))  # GSTR-1, GSTR-3B
    taxable_value = Column(Float)
    igst = Column(Float, default=0)
    cgst = Column(Float, default=0)
    sgst = Column(Float, default=0)
    cess = Column(Float, default=0)
    itc_available = Column(Float, default=0)  # Input Tax Credit
    itc_utilized = Column(Float, default=0)
    filed_date = Column(DateTime(timezone=True))
    status = Column(String(50))  # Filed, Pending, Revised
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class BankTransaction(Base):
    __tablename__ = "bank_transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, nullable=False, index=True)
    transaction_date = Column(DateTime(timezone=True))
    description = Column(Text)
    reference_number = Column(String(100))
    debit = Column(Float, default=0)
    credit = Column(Float, default=0)
    balance = Column(Float)
    category = Column(String(100))  # Auto-categorized
    subcategory = Column(String(100))
    bank_name = Column(String(100))
    account_number = Column(String(50))
    is_reconciled = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    action = Column(String(100))  # CREATE, UPDATE, DELETE, VIEW
    entity_type = Column(String(50))  # Company, Document, Assessment, etc.
    entity_id = Column(Integer)
    changes = Column(JSON)  # Before/after values
    ip_address = Column(String(50))
    user_agent = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
