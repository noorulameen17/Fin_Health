from typing import Dict, Any, List
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class FinancialAnalyzer:
    """Service for analyzing financial data and calculating metrics"""
    
    @staticmethod
    def calculate_liquidity_ratios(current_assets: float, current_liabilities: float, 
                                   inventory: float = 0, cash: float = 0) -> Dict[str, float]:
        """Calculate liquidity ratios"""
        ratios = {}
        
        if current_liabilities > 0:
            # Current Ratio
            ratios['current_ratio'] = current_assets / current_liabilities
            
            # Quick Ratio (Acid Test)
            quick_assets = current_assets - inventory
            ratios['quick_ratio'] = quick_assets / current_liabilities
            
            # Cash Ratio
            ratios['cash_ratio'] = cash / current_liabilities
        else:
            ratios['current_ratio'] = 0
            ratios['quick_ratio'] = 0
            ratios['cash_ratio'] = 0
        
        return ratios
    
    @staticmethod
    def calculate_profitability_ratios(revenue: float, gross_profit: float, 
                                       net_profit: float, total_assets: float, 
                                       equity: float) -> Dict[str, float]:
        """Calculate profitability ratios"""
        ratios = {}
        
        if revenue > 0:
            ratios['gross_profit_margin'] = (gross_profit / revenue) * 100
            ratios['net_profit_margin'] = (net_profit / revenue) * 100
        else:
            ratios['gross_profit_margin'] = 0
            ratios['net_profit_margin'] = 0
        
        if total_assets > 0:
            ratios['return_on_assets'] = (net_profit / total_assets) * 100
        else:
            ratios['return_on_assets'] = 0
        
        if equity > 0:
            ratios['return_on_equity'] = (net_profit / equity) * 100
        else:
            ratios['return_on_equity'] = 0
        
        return ratios
    
    @staticmethod
    def calculate_leverage_ratios(total_debt: float, total_assets: float, 
                                  equity: float, ebit: float, 
                                  interest_expense: float) -> Dict[str, float]:
        """Calculate leverage ratios"""
        ratios = {}
        
        if equity > 0:
            ratios['debt_to_equity'] = total_debt / equity
        else:
            ratios['debt_to_equity'] = 0
        
        if total_assets > 0:
            ratios['debt_to_assets'] = total_debt / total_assets
        else:
            ratios['debt_to_assets'] = 0
        
        if interest_expense > 0:
            ratios['interest_coverage'] = ebit / interest_expense
        else:
            ratios['interest_coverage'] = 0
        
        return ratios
    
    @staticmethod
    def calculate_efficiency_ratios(revenue: float, total_assets: float, 
                                    inventory: float, cogs: float,
                                    accounts_receivable: float) -> Dict[str, float]:
        """Calculate efficiency ratios"""
        ratios = {}
        
        if total_assets > 0:
            ratios['asset_turnover'] = revenue / total_assets
        else:
            ratios['asset_turnover'] = 0
        
        if inventory > 0 and cogs > 0:
            ratios['inventory_turnover'] = cogs / inventory
            ratios['days_inventory'] = 365 / ratios['inventory_turnover']
        else:
            ratios['inventory_turnover'] = 0
            ratios['days_inventory'] = 0
        
        if accounts_receivable > 0 and revenue > 0:
            ratios['receivables_turnover'] = revenue / accounts_receivable
            ratios['days_receivable'] = 365 / ratios['receivables_turnover']
        else:
            ratios['receivables_turnover'] = 0
            ratios['days_receivable'] = 0
        
        return ratios
    
    @staticmethod
    def calculate_working_capital(current_assets: float, current_liabilities: float) -> float:
        """Calculate working capital"""
        return current_assets - current_liabilities
    
    @staticmethod
    def calculate_free_cash_flow(operating_cash_flow: float, capital_expenditure: float) -> float:
        """Calculate free cash flow"""
        return operating_cash_flow - capital_expenditure
    
    @staticmethod
    def analyze_cash_flow_trend(cash_flows: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cash flow trends"""
        if not cash_flows:
            return {"trend": "insufficient_data"}
        
        df = pd.DataFrame(cash_flows)
        
        analysis = {
            "trend": "stable",
            "volatility": "low",
            "average_operating_cf": 0,
            "average_investing_cf": 0,
            "average_financing_cf": 0
        }
        
        if 'operating_cash_flow' in df.columns:
            analysis['average_operating_cf'] = df['operating_cash_flow'].mean()
            
            # Determine trend
            if len(df) >= 3:
                recent_avg = df['operating_cash_flow'].tail(3).mean()
                older_avg = df['operating_cash_flow'].head(3).mean()
                
                if recent_avg > older_avg * 1.1:
                    analysis['trend'] = "improving"
                elif recent_avg < older_avg * 0.9:
                    analysis['trend'] = "declining"
        
        if 'investing_cash_flow' in df.columns:
            analysis['average_investing_cf'] = df['investing_cash_flow'].mean()
        
        if 'financing_cash_flow' in df.columns:
            analysis['average_financing_cf'] = df['financing_cash_flow'].mean()
        
        return analysis
    
    @staticmethod
    def forecast_revenue(historical_revenue: List[float], periods: int = 12) -> List[float]:
        """Simple revenue forecasting using linear regression"""
        if len(historical_revenue) < 2:
            return historical_revenue
        
        # Create time series
        x = np.arange(len(historical_revenue))
        y = np.array(historical_revenue)
        
        # Fit linear regression
        coefficients = np.polyfit(x, y, 1)
        polynomial = np.poly1d(coefficients)
        
        # Forecast
        future_x = np.arange(len(historical_revenue), len(historical_revenue) + periods)
        forecast = polynomial(future_x)
        
        # Ensure non-negative forecasts
        forecast = np.maximum(forecast, 0)
        
        return forecast.tolist()
    
    @staticmethod
    def calculate_burn_rate(expenses: float, period_months: int = 1) -> float:
        """Calculate monthly burn rate"""
        if period_months == 0:
            return 0
        return expenses / period_months
    
    @staticmethod
    def calculate_runway(cash_balance: float, burn_rate: float) -> float:
        """Calculate runway in months"""
        if burn_rate <= 0:
            return float('inf')
        return cash_balance / burn_rate
    
    @staticmethod
    def assess_financial_health(metrics: Dict[str, float]) -> Dict[str, Any]:
        """Assess overall financial health based on key metrics"""
        score = 100  # Start with perfect score
        issues = []
        strengths = []
        
        # Liquidity Assessment
        current_ratio = metrics.get('current_ratio', 0)
        if current_ratio < 1.0:
            score -= 15
            issues.append("Low liquidity - current ratio below 1.0")
        elif current_ratio > 1.5:
            strengths.append("Strong liquidity position")
        
        # Profitability Assessment
        net_margin = metrics.get('net_profit_margin', 0)
        if net_margin < 0:
            score -= 20
            issues.append("Negative profit margin")
        elif net_margin > 10:
            strengths.append("Healthy profit margins")
        
        # Leverage Assessment
        debt_to_equity = metrics.get('debt_to_equity', 0)
        if debt_to_equity > 2.0:
            score -= 15
            issues.append("High debt-to-equity ratio")
        elif debt_to_equity < 0.5:
            strengths.append("Low debt burden")
        
        # Efficiency Assessment
        asset_turnover = metrics.get('asset_turnover', 0)
        if asset_turnover < 0.5:
            score -= 10
            issues.append("Low asset utilization")
        elif asset_turnover > 1.5:
            strengths.append("Efficient asset utilization")
        
        # Determine risk level
        if score >= 80:
            risk_level = "Low"
        elif score >= 60:
            risk_level = "Medium"
        elif score >= 40:
            risk_level = "High"
        else:
            risk_level = "Critical"
        
        return {
            "health_score": max(0, score),
            "risk_level": risk_level,
            "issues": issues,
            "strengths": strengths
        }
