from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.models.models import Assessment, Company, FinancialMetrics, CreditScore, RiskLevel
from app.services.financial_analyzer import FinancialAnalyzer
from app.services.ai_service import ai_service
from pydantic import BaseModel
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class AssessmentRequest(BaseModel):
    company_id: int
    language: str = "en"

class AssessmentResponse(BaseModel):
    id: int
    company_id: int
    financial_health_score: float
    risk_level: str
    strengths: List[dict] = []
    weaknesses: List[dict] = []
    opportunities: List[dict] = []
    threats: List[dict] = []
    cost_optimization: List[dict] = []
    revenue_enhancement: List[dict] = []
    working_capital_tips: List[dict] = []
    tax_optimization: List[dict] = []
    recommended_products: List[dict] = []
    executive_summary: str = ""
    language: str = "en"
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

@router.post("/generate", response_model=AssessmentResponse)
async def generate_assessment(
    request: AssessmentRequest,
    db: Session = Depends(get_db)
):
    """Generate comprehensive financial health assessment"""
    
    # Verify company exists
    company = db.query(Company).filter(Company.id == request.company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    try:
        # Get latest financial metrics
        metrics = db.query(FinancialMetrics).filter(
            FinancialMetrics.company_id == request.company_id
        ).order_by(FinancialMetrics.created_at.desc()).first()
        
        if not metrics:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No financial metrics found. Please upload and process financial documents first."
            )
        
        # Convert metrics to dictionary
        financial_data = {
            "revenue": metrics.total_revenue or 0,
            "gross_profit": metrics.gross_profit or 0,
            "net_profit": metrics.net_profit or 0,
            "current_ratio": metrics.current_ratio or 0,
            "quick_ratio": metrics.quick_ratio or 0,
            "debt_to_equity": metrics.debt_to_equity or 0,
            "net_profit_margin": metrics.net_profit_margin or 0,
            "return_on_assets": metrics.return_on_assets or 0,
            "return_on_equity": metrics.return_on_equity or 0,
            "working_capital": metrics.working_capital or 0
        }
        
        # Assess financial health
        analyzer = FinancialAnalyzer()
        health_assessment = analyzer.assess_financial_health(financial_data)
        
        # Get company info
        company_info = {
            "name": company.name,
            "industry": company.industry.value
        }
        
        # Generate AI insights
        insights = await ai_service.generate_insights(financial_data, company_info)
        
        # Generate recommendations
        recommendations = await ai_service.generate_recommendations(
            financial_data,
            company.industry.value
        )
        
        # Get credit score
        credit_score_record = db.query(CreditScore).filter(
            CreditScore.company_id == request.company_id
        ).order_by(CreditScore.created_at.desc()).first()
        
        credit_score = credit_score_record.score if credit_score_record else 600
        
        # Recommend financial products
        products = await ai_service.recommend_financial_products(
            credit_score,
            company.industry.value,
            financial_data
        )
        
        # Create assessment data for summary
        assessment_data = {
            "financial_health_score": health_assessment['health_score'],
            "risk_level": health_assessment['risk_level'],
            "strengths": insights.get('strengths', []),
            "weaknesses": insights.get('weaknesses', []),
            "key_metrics": financial_data
        }
        
        # Generate executive summary
        executive_summary = await ai_service.generate_executive_summary(
            assessment_data,
            request.language
        )
        
        # Create assessment record
        assessment = Assessment(
            company_id=request.company_id,
            financial_health_score=health_assessment['health_score'],
            risk_level=RiskLevel[health_assessment['risk_level'].upper()],
            strengths=insights.get('strengths', []),
            weaknesses=insights.get('weaknesses', []),
            opportunities=insights.get('opportunities', []),
            threats=insights.get('threats', []),
            cost_optimization=recommendations.get('cost_optimization', []),
            revenue_enhancement=recommendations.get('revenue_enhancement', []),
            working_capital_tips=recommendations.get('working_capital_tips', []),
            tax_optimization=recommendations.get('tax_optimization', []),
            recommended_products=products,
            executive_summary=executive_summary,
            language=request.language,
            revenue_forecast=[],
            cash_flow_forecast=[],
            industry_benchmark={}
        )
        
        db.add(assessment)
        db.commit()
        db.refresh(assessment)
        
        return assessment
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating assessment: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating assessment: {str(e)}"
        )

@router.get("/company/{company_id}", response_model=List[AssessmentResponse])
async def get_company_assessments(
    company_id: int,
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get all assessments for a company"""
    
    assessments = db.query(Assessment).filter(
        Assessment.company_id == company_id
    ).order_by(Assessment.created_at.desc()).limit(limit).all()
    
    return assessments

@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(assessment_id: int, db: Session = Depends(get_db)):
    """Get assessment by ID"""
    
    assessment = db.query(Assessment).filter(
        Assessment.id == assessment_id
    ).first()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment not found"
        )
    
    return assessment

@router.post("/calculate-metrics/{company_id}")
async def calculate_metrics(
    company_id: int,
    current_assets: float,
    current_liabilities: float,
    total_assets: float,
    total_liabilities: float,
    equity: float,
    revenue: float,
    gross_profit: float,
    net_profit: float,
    operating_profit: float = 0,
    ebitda: float = 0,
    inventory: float = 0,
    cash: float = 0,
    accounts_receivable: float = 0,
    accounts_payable: float = 0,
    cogs: float = 0,
    interest_expense: float = 0,
    operating_cash_flow: float = 0,
    investing_cash_flow: float = 0,
    financing_cash_flow: float = 0,
    db: Session = Depends(get_db)
):
    """Calculate and store financial metrics"""
    
    # Verify company exists
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    try:
        analyzer = FinancialAnalyzer()
        
        # Calculate all ratios
        liquidity = analyzer.calculate_liquidity_ratios(
            current_assets, current_liabilities, inventory, cash
        )
        
        profitability = analyzer.calculate_profitability_ratios(
            revenue, gross_profit, net_profit, total_assets, equity
        )
        
        total_debt = total_liabilities
        leverage = analyzer.calculate_leverage_ratios(
            total_debt, total_assets, equity, ebitda or operating_profit, interest_expense
        )
        
        efficiency = analyzer.calculate_efficiency_ratios(
            revenue, total_assets, inventory, cogs, accounts_receivable
        )
        
        working_capital = analyzer.calculate_working_capital(
            current_assets, current_liabilities
        )
        
        # Create metrics record
        metrics = FinancialMetrics(
            company_id=company_id,
            total_revenue=revenue,
            gross_profit=gross_profit,
            net_profit=net_profit,
            operating_profit=operating_profit,
            ebitda=ebitda,
            current_ratio=liquidity['current_ratio'],
            quick_ratio=liquidity['quick_ratio'],
            cash_ratio=liquidity['cash_ratio'],
            gross_profit_margin=profitability['gross_profit_margin'],
            net_profit_margin=profitability['net_profit_margin'],
            return_on_assets=profitability['return_on_assets'],
            return_on_equity=profitability['return_on_equity'],
            debt_to_equity=leverage['debt_to_equity'],
            debt_to_assets=leverage['debt_to_assets'],
            interest_coverage=leverage['interest_coverage'],
            asset_turnover=efficiency['asset_turnover'],
            inventory_turnover=efficiency['inventory_turnover'],
            receivables_turnover=efficiency['receivables_turnover'],
            operating_cash_flow=operating_cash_flow,
            investing_cash_flow=investing_cash_flow,
            financing_cash_flow=financing_cash_flow,
            working_capital=working_capital,
            accounts_receivable=accounts_receivable,
            accounts_payable=accounts_payable,
            inventory=inventory
        )
        
        db.add(metrics)
        db.commit()
        db.refresh(metrics)
        
        return {
            "message": "Metrics calculated successfully",
            "metrics": {
                "liquidity": liquidity,
                "profitability": profitability,
                "leverage": leverage,
                "efficiency": efficiency,
                "working_capital": working_capital
            }
        }
        
    except Exception as e:
        logger.error(f"Error calculating metrics: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error calculating metrics: {str(e)}"
        )
