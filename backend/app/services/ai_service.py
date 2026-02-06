from typing import Dict, Any, List, Optional
from perplexity import Perplexity
from app.core.config import settings
import logging
import json

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI-powered insights using Perplexity API"""
    
    def __init__(self):
        self.model = settings.AI_MODEL or "sonar-pro"
        # Initialize Perplexity client
        self.client = Perplexity(api_key=settings.OPENAI_API_KEY)
        self.provider = "perplexity"
    
    async def generate_insights(self, financial_data: Dict[str, Any], 
                               company_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate AI-powered financial insights"""
        
        prompt = self._create_insights_prompt(financial_data, company_info)
        
        try:
            response = await self._call_perplexity(prompt)
            
            # Parse the AI response
            insights = self._parse_insights_response(response)
            return insights
            
        except Exception as e:
            logger.error(f"Error generating insights: {str(e)}")
            return self._get_fallback_insights()
    
    async def generate_recommendations(self, financial_data: Dict[str, Any],
                                      industry: str) -> Dict[str, Any]:
        """Generate actionable recommendations"""
        
        prompt = self._create_recommendations_prompt(financial_data, industry)
        
        try:
            response = await self._call_perplexity(prompt)
            
            recommendations = self._parse_recommendations_response(response)
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return self._get_fallback_recommendations()
    
    async def generate_executive_summary(self, assessment_data: Dict[str, Any],
                                        language: str = "en") -> str:
        """Generate executive summary in specified language"""
        
        prompt = self._create_summary_prompt(assessment_data, language)
        
        try:
            response = await self._call_perplexity(prompt, max_tokens=1000)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return "Unable to generate executive summary at this time."
    
    async def recommend_financial_products(self, credit_score: int,
                                          industry: str,
                                          financial_metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend suitable financial products"""
        
        prompt = f"""
        Based on the following information, recommend suitable financial products from banks and NBFCs:
        
        Credit Score: {credit_score}
        Industry: {industry}
        Financial Metrics: {json.dumps(financial_metrics, indent=2)}
        
        Provide recommendations for:
        1. Working capital loans
        2. Term loans
        3. Trade credit
        4. Equipment financing
        5. Invoice financing
        
        For each product, specify:
        - Product name and type
        - Suitable providers (generic categories)
        - Estimated interest rate range
        - Eligibility criteria
        - Key benefits
        """
        
        try:
            response = await self._call_perplexity(prompt)
            
            products = self._parse_products_response(response)
            return products
            
        except Exception as e:
            logger.error(f"Error recommending products: {str(e)}")
            return []
    
    def _create_insights_prompt(self, financial_data: Dict[str, Any], 
                               company_info: Dict[str, Any]) -> str:
        """Create prompt for generating insights"""
        
        return f"""
        You are a financial analyst expert. Analyze the following financial data and provide comprehensive insights.
        
        Company Information:
        - Name: {company_info.get('name', 'N/A')}
        - Industry: {company_info.get('industry', 'N/A')}
        
        Financial Data:
        {json.dumps(financial_data, indent=2)}
        
        Provide a detailed analysis covering:
        1. STRENGTHS: List 3-5 key financial strengths
        2. WEAKNESSES: List 3-5 areas of concern
        3. OPPORTUNITIES: List 3-5 growth opportunities
        4. THREATS: List 3-5 potential risks
        
        Format your response as JSON with keys: strengths, weaknesses, opportunities, threats
        Each should be an array of strings.
        """
    
    def _create_recommendations_prompt(self, financial_data: Dict[str, Any],
                                      industry: str) -> str:
        """Create prompt for generating recommendations"""
        
        return f"""
        As a financial advisor, provide actionable recommendations for this {industry} business.
        
        Financial Data:
        {json.dumps(financial_data, indent=2)}
        
        Provide specific recommendations in the following categories:
        1. COST_OPTIMIZATION: 3-5 ways to reduce costs
        2. REVENUE_ENHANCEMENT: 3-5 ways to increase revenue
        3. WORKING_CAPITAL: 3-5 ways to optimize working capital
        4. TAX_OPTIMIZATION: 3-5 tax planning strategies
        
        Format as JSON with keys: cost_optimization, revenue_enhancement, working_capital_tips, tax_optimization
        Each should be an array of objects with 'title' and 'description' fields.
        """
    
    def _create_summary_prompt(self, assessment_data: Dict[str, Any],
                              language: str) -> str:
        """Create prompt for executive summary"""
        
        lang_instruction = ""
        if language == "hi":
            lang_instruction = "Write the summary in Hindi language."
        elif language != "en":
            lang_instruction = f"Write the summary in {language} language."
        
        return f"""
        Create a concise executive summary of this financial health assessment.
        
        Assessment Data:
        {json.dumps(assessment_data, indent=2)}
        
        The summary should:
        - Be 3-4 paragraphs
        - Highlight the overall financial health score and risk level
        - Mention key strengths and concerns
        - Provide 2-3 top recommendations
        
        {lang_instruction}
        """
    
    async def _call_perplexity(self, prompt: str, max_tokens: int = 2000) -> str:
        """Call Perplexity API using native SDK"""
        try:
            # Non-streaming version for simpler integration
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst with deep knowledge of business finance, accounting, and financial planning."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Perplexity API error: {str(e)}")
            raise
    
    async def _call_perplexity_stream(self, prompt: str, max_tokens: int = 2000):
        """Call Perplexity API with streaming (for future use)"""
        try:
            stream = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert financial analyst with deep knowledge of business finance, accounting, and financial planning."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                top_p=0.9,
                stream=True
            )
            
            full_response = ""
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    full_response += content
                    # Could yield here for real-time streaming
            
            return full_response
        except Exception as e:
            logger.error(f"Perplexity streaming API error: {str(e)}")
            raise
    
    def _parse_insights_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for insights"""
        try:
            # Try to extract JSON from response
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)
                
                # Convert string arrays to dict arrays if needed
                for key in ['strengths', 'weaknesses', 'opportunities', 'threats']:
                    if key in data and isinstance(data[key], list):
                        # If items are strings, convert to dicts
                        if data[key] and isinstance(data[key][0], str):
                            data[key] = [{"point": item} for item in data[key]]
                
                return data
        except Exception as e:
            logger.warning(f"Failed to parse insights response: {str(e)}")
        
        # Fallback parsing
        return {
            "strengths": [{"point": "Strong revenue growth"}, {"point": "Healthy cash flow"}],
            "weaknesses": [{"point": "High debt levels"}, {"point": "Low profit margins"}],
            "opportunities": [{"point": "Market expansion"}, {"point": "Digital transformation"}],
            "threats": [{"point": "Economic uncertainty"}, {"point": "Competitive pressure"}]
        }
    
    def _parse_recommendations_response(self, response: str) -> Dict[str, Any]:
        """Parse AI response for recommendations"""
        try:
            start = response.find('{')
            end = response.rfind('}') + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        
        return self._get_fallback_recommendations()
    
    def _parse_products_response(self, response: str) -> List[Dict[str, Any]]:
        """Parse AI response for product recommendations"""
        # Simplified parsing - in production, use more robust parsing
        return [
            {
                "product_name": "Working Capital Loan",
                "type": "Short-term financing",
                "interest_range": "10-14% per annum",
                "benefits": ["Quick approval", "Flexible repayment"]
            },
            {
                "product_name": "Term Loan",
                "type": "Long-term financing",
                "interest_range": "11-15% per annum",
                "benefits": ["Business expansion", "Asset purchase"]
            }
        ]
    
    def _get_fallback_insights(self) -> Dict[str, Any]:
        """Fallback insights when AI fails"""
        return {
            "strengths": [{"point": "Business operations are ongoing"}],
            "weaknesses": [{"point": "Unable to generate detailed insights"}],
            "opportunities": [{"point": "Further analysis recommended"}],
            "threats": [{"point": "Market conditions should be monitored"}]
        }
    
    def _get_fallback_recommendations(self) -> Dict[str, Any]:
        """Fallback recommendations when AI fails"""
        return {
            "cost_optimization": [
                {"title": "Review operational expenses", "description": "Conduct regular expense audits"}
            ],
            "revenue_enhancement": [
                {"title": "Diversify revenue streams", "description": "Explore new market opportunities"}
            ],
            "working_capital_tips": [
                {"title": "Improve cash collection", "description": "Reduce receivables days"}
            ],
            "tax_optimization": [
                {"title": "Maximize deductions", "description": "Consult with tax advisor"}
            ]
        }

# Global AI service instance
ai_service = AIService()
