import pandas as pd
import pdfplumber
from typing import Dict, Any
import logging
import json

logger = logging.getLogger(__name__)

class DocumentParser:
    """Service for parsing financial documents in various formats"""
    
    @staticmethod
    def parse_csv(file_path: str) -> pd.DataFrame:
        """Parse CSV file"""
        try:
            df = pd.read_csv(file_path)
            return df
        except Exception as e:
            logger.error(f"Error parsing CSV: {str(e)}")
            raise
    
    @staticmethod
    def parse_excel(file_path: str) -> pd.DataFrame:
        """Parse Excel file"""
        try:
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            logger.error(f"Error parsing Excel: {str(e)}")
            raise
    
    @staticmethod
    def parse_pdf(file_path: str) -> Dict[str, Any]:
        """Parse PDF file and extract tables"""
        try:
            data = {
                "text": "",
                "tables": []
            }
            
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    # Extract text
                    text = page.extract_text()
                    if text:
                        data["text"] += text + "\n"
                    
                    # Extract tables
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            data["tables"].append(table)
            
            return data
        except Exception as e:
            logger.error(f"Error parsing PDF: {str(e)}")
            raise
    
    @staticmethod
    def extract_financial_data(df: pd.DataFrame) -> Dict[str, Any]:
        """Extract key financial metrics from dataframe"""
        financial_data = {}
        
        try:
            # Try to identify common financial statement patterns
            df_lower = df.copy()
            
            # Convert column names to lowercase for easier matching
            if not df.empty:
                df_lower.columns = [str(col).lower().strip() for col in df.columns]
            
            # Try to identify the account name and value columns
            account_col = None
            value_col = None
            
            # Look for account/description column
            for col in df_lower.columns:
                col_str = str(col).lower()
                if any(keyword in col_str for keyword in ['account', 'description', 'item', 'category', 'line']):
                    account_col = col
                    break
            
            # If no specific column found, use first column
            if account_col is None and len(df_lower.columns) > 0:
                account_col = df_lower.columns[0]
            
            # Look for value column (numeric)
            numeric_cols = df_lower.select_dtypes(include=['number']).columns.tolist()
            if numeric_cols:
                value_col = numeric_cols[-1]  # Use last numeric column (usually the most recent period)
            
            if account_col and value_col:
                # Create a mapping of account names to values
                account_map = {}
                for _, row in df_lower.iterrows():
                    account_name = str(row[account_col]).lower().strip()
                    value = row[value_col] if pd.notna(row[value_col]) else 0
                    account_map[account_name] = value
                
                # Extract specific metrics based on common patterns
                # Revenue
                for key in ['revenue', 'sales', 'total revenue', 'total sales', 'net sales', 'net revenue']:
                    if key in account_map:
                        financial_data['revenue'] = abs(float(account_map[key]))
                        break
                
                # Gross Profit
                for key in ['gross profit', 'gross margin']:
                    if key in account_map:
                        financial_data['gross_profit'] = abs(float(account_map[key]))
                        break
                
                # Net Profit
                for key in ['net profit', 'net income', 'net earnings', 'profit after tax', 'net profit after tax']:
                    if key in account_map:
                        financial_data['net_profit'] = abs(float(account_map[key]))
                        break
                
                # Operating Profit
                for key in ['operating profit', 'operating income', 'ebit']:
                    if key in account_map:
                        financial_data['operating_profit'] = abs(float(account_map[key]))
                        break
                
                # EBITDA
                for key in ['ebitda']:
                    if key in account_map:
                        financial_data['ebitda'] = abs(float(account_map[key]))
                        break
                
                # Assets
                for key in ['total assets', 'assets']:
                    if key in account_map:
                        financial_data['total_assets'] = abs(float(account_map[key]))
                        break
                
                for key in ['current assets', 'total current assets']:
                    if key in account_map:
                        financial_data['current_assets'] = abs(float(account_map[key]))
                        break
                
                for key in ['cash', 'cash and cash equivalents', 'cash & equivalents']:
                    if key in account_map:
                        financial_data['cash'] = abs(float(account_map[key]))
                        break
                
                for key in ['inventory', 'inventories']:
                    if key in account_map:
                        financial_data['inventory'] = abs(float(account_map[key]))
                        break
                
                for key in ['accounts receivable', 'receivables', 'trade receivables']:
                    if key in account_map:
                        financial_data['accounts_receivable'] = abs(float(account_map[key]))
                        break
                
                # Liabilities
                for key in ['total liabilities', 'liabilities']:
                    if key in account_map:
                        financial_data['total_liabilities'] = abs(float(account_map[key]))
                        break
                
                for key in ['current liabilities', 'total current liabilities']:
                    if key in account_map:
                        financial_data['current_liabilities'] = abs(float(account_map[key]))
                        break
                
                for key in ['accounts payable', 'payables', 'trade payables']:
                    if key in account_map:
                        financial_data['accounts_payable'] = abs(float(account_map[key]))
                        break
                
                for key in ['long-term debt', 'long term debt', 'debt']:
                    if key in account_map:
                        financial_data['long_term_debt'] = abs(float(account_map[key]))
                        break
                
                # Equity
                for key in ['equity', 'total equity', 'shareholders equity', "shareholders' equity", 'owners equity']:
                    if key in account_map:
                        financial_data['equity'] = abs(float(account_map[key]))
                        break
                
                # Expenses
                for key in ['cogs', 'cost of goods sold', 'cost of sales']:
                    if key in account_map:
                        financial_data['cogs'] = abs(float(account_map[key]))
                        break
            
            # Store raw data as well
            financial_data['raw_data'] = df.to_dict(orient='records')
            
        except Exception as e:
            logger.error(f"Error extracting financial data: {str(e)}")
            financial_data['error'] = str(e)
        
        return financial_data
    
    @staticmethod
    def normalize_financial_statement(data: Dict[str, Any], statement_type: str) -> Dict[str, Any]:
        """Normalize financial statement data to a standard format"""
        normalized = {
            "statement_type": statement_type,
            "data": data,
            "extracted_metrics": {}
        }
        
        # Add specific normalization logic based on statement type
        if statement_type == "income_statement":
            normalized["extracted_metrics"] = {
                "revenue": data.get("revenue", 0),
                "expenses": data.get("expenses", 0),
                "gross_profit": data.get("gross_profit", 0),
                "net_profit": data.get("net_profit", 0),
                "operating_profit": data.get("operating_profit", 0)
            }
        elif statement_type == "balance_sheet":
            normalized["extracted_metrics"] = {
                "total_assets": data.get("total_assets", 0),
                "current_assets": data.get("current_assets", 0),
                "total_liabilities": data.get("total_liabilities", 0),
                "current_liabilities": data.get("current_liabilities", 0),
                "equity": data.get("equity", 0)
            }
        elif statement_type == "cash_flow":
            normalized["extracted_metrics"] = {
                "operating_cash_flow": data.get("operating_cash_flow", 0),
                "investing_cash_flow": data.get("investing_cash_flow", 0),
                "financing_cash_flow": data.get("financing_cash_flow", 0)
            }
        
        return normalized
