from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.core.config import settings
from app.models.models import FinancialDocument, Company, FinancialMetrics
from app.services.document_parser import DocumentParser
from app.services.financial_analyzer import FinancialAnalyzer
from pydantic import BaseModel
from datetime import datetime
import os
import shutil
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

async def auto_calculate_metrics(company_id: int, document_type: str, normalized_data: dict, db: Session):
    """Automatically calculate and update financial metrics from processed documents"""
    try:
        # Get all processed documents for this company
        documents = db.query(FinancialDocument).filter(
            FinancialDocument.company_id == company_id,
            FinancialDocument.processed == True
        ).all()
        
        # Aggregate data from all documents
        aggregated_data = {
            "revenue": 0,
            "gross_profit": 0,
            "net_profit": 0,
            "operating_profit": 0,
            "ebitda": 0,
            "current_assets": 0,
            "current_liabilities": 0,
            "total_assets": 0,
            "total_liabilities": 0,
            "equity": 0,
            "inventory": 0,
            "cash": 0,
            "accounts_receivable": 0,
            "accounts_payable": 0,
            "cogs": 0,
            "operating_cash_flow": 0,
            "investing_cash_flow": 0,
            "financing_cash_flow": 0
        }
        
        for doc in documents:
            if doc.data and isinstance(doc.data, dict):
                extracted = doc.data.get("extracted_metrics", {})
                
                # Merge extracted metrics
                for key in aggregated_data.keys():
                    if key in extracted:
                        aggregated_data[key] = extracted[key]
        
        # Only create metrics if we have meaningful data
        if aggregated_data["revenue"] > 0 or aggregated_data["total_assets"] > 0:
            analyzer = FinancialAnalyzer()
            
            # Calculate working capital
            working_capital = analyzer.calculate_working_capital(
                aggregated_data["current_assets"],
                aggregated_data["current_liabilities"]
            )
            
            # Calculate ratios
            current_ratio = 0
            quick_ratio = 0
            cash_ratio = 0
            
            if aggregated_data["current_liabilities"] > 0:
                current_ratio = aggregated_data["current_assets"] / aggregated_data["current_liabilities"]
                quick_assets = aggregated_data["current_assets"] - aggregated_data["inventory"]
                quick_ratio = quick_assets / aggregated_data["current_liabilities"]
                cash_ratio = aggregated_data["cash"] / aggregated_data["current_liabilities"]
            
            # Profitability ratios
            gross_profit_margin = 0
            net_profit_margin = 0
            return_on_assets = 0
            return_on_equity = 0
            
            if aggregated_data["revenue"] > 0:
                gross_profit_margin = (aggregated_data["gross_profit"] / aggregated_data["revenue"]) * 100
                net_profit_margin = (aggregated_data["net_profit"] / aggregated_data["revenue"]) * 100
            
            if aggregated_data["total_assets"] > 0:
                return_on_assets = (aggregated_data["net_profit"] / aggregated_data["total_assets"]) * 100
            
            if aggregated_data["equity"] > 0:
                return_on_equity = (aggregated_data["net_profit"] / aggregated_data["equity"]) * 100
            
            # Leverage ratios
            debt_to_equity = 0
            debt_to_assets = 0
            
            if aggregated_data["equity"] > 0:
                debt_to_equity = aggregated_data["total_liabilities"] / aggregated_data["equity"]
            
            if aggregated_data["total_assets"] > 0:
                debt_to_assets = aggregated_data["total_liabilities"] / aggregated_data["total_assets"]
            
            # Create or update metrics record
            metrics = FinancialMetrics(
                company_id=company_id,
                total_revenue=aggregated_data["revenue"],
                gross_profit=aggregated_data["gross_profit"],
                net_profit=aggregated_data["net_profit"],
                operating_profit=aggregated_data["operating_profit"],
                ebitda=aggregated_data["ebitda"],
                current_ratio=current_ratio,
                quick_ratio=quick_ratio,
                cash_ratio=cash_ratio,
                gross_profit_margin=gross_profit_margin,
                net_profit_margin=net_profit_margin,
                return_on_assets=return_on_assets,
                return_on_equity=return_on_equity,
                debt_to_equity=debt_to_equity,
                debt_to_assets=debt_to_assets,
                interest_coverage=0,
                asset_turnover=0,
                inventory_turnover=0,
                receivables_turnover=0,
                operating_cash_flow=aggregated_data["operating_cash_flow"],
                investing_cash_flow=aggregated_data["investing_cash_flow"],
                financing_cash_flow=aggregated_data["financing_cash_flow"],
                working_capital=working_capital,
                accounts_receivable=aggregated_data["accounts_receivable"],
                accounts_payable=aggregated_data["accounts_payable"],
                inventory=aggregated_data["inventory"]
            )
            
            db.add(metrics)
            db.commit()
            logger.info(f"Auto-calculated metrics for company {company_id}")
            
    except Exception as e:
        logger.error(f"Error auto-calculating metrics: {str(e)}")
        # Don't raise exception - metrics calculation is optional

class DocumentResponse(BaseModel):
    id: int
    company_id: int
    document_type: str
    file_name: str
    uploaded_at: datetime
    processed: bool
    
    class Config:
        from_attributes = True

@router.post("/upload/{company_id}", response_model=DocumentResponse)
async def upload_document(
    company_id: int,
    document_type: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a financial document"""
    
    # Verify company exists
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    # Validate file extension
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Create company-specific upload directory
    company_dir = os.path.join(settings.UPLOAD_DIR, str(company_id))
    os.makedirs(company_dir, exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{timestamp}_{file.filename}"
    file_path = os.path.join(company_dir, safe_filename)
    
    # Save file
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving file"
        )
    
    # Create database record
    db_document = FinancialDocument(
        company_id=company_id,
        document_type=document_type,
        file_name=file.filename,
        file_path=file_path,
        file_type=file_ext.replace('.', ''),
        processed=False
    )
    
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    
    return db_document

@router.post("/process/{document_id}")
async def process_document(document_id: int, db: Session = Depends(get_db)):
    """Process an uploaded document"""
    
    document = db.query(FinancialDocument).filter(
        FinancialDocument.id == document_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    if document.processed:
        return {"message": "Document already processed", "data": document.data}
    
    try:
        parser = DocumentParser()
        
        # Parse based on file type
        if document.file_type == 'csv':
            df = parser.parse_csv(document.file_path)
            financial_data = parser.extract_financial_data(df)
        elif document.file_type in ['xlsx', 'xls']:
            df = parser.parse_excel(document.file_path)
            financial_data = parser.extract_financial_data(df)
        elif document.file_type == 'pdf':
            pdf_data = parser.parse_pdf(document.file_path)
            financial_data = pdf_data
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type"
            )
        
        # Normalize data
        normalized_data = parser.normalize_financial_statement(
            financial_data,
            document.document_type
        )
        
        # Update document record
        document.data = normalized_data
        document.processed = True
        document.processed_at = datetime.now()
        
        db.commit()
        db.refresh(document)
        
        # Auto-calculate metrics if we have the necessary data
        await auto_calculate_metrics(document.company_id, document.document_type, normalized_data, db)
        
        return {
            "message": "Document processed successfully",
            "data": normalized_data
        }
        
    except Exception as e:
        logger.error(f"Error processing document: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing document: {str(e)}"
        )

@router.get("/company/{company_id}", response_model=List[DocumentResponse])
async def get_company_documents(company_id: int, db: Session = Depends(get_db)):
    """Get all documents for a company"""
    
    documents = db.query(FinancialDocument).filter(
        FinancialDocument.company_id == company_id
    ).order_by(FinancialDocument.uploaded_at.desc()).all()
    
    return documents

@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """Get document by ID"""
    
    document = db.query(FinancialDocument).filter(
        FinancialDocument.id == document_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    return document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document"""
    
    document = db.query(FinancialDocument).filter(
        FinancialDocument.id == document_id
    ).first()
    
    if not document:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
    
    # Delete physical file
    try:
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
    except Exception as e:
        logger.error(f"Error deleting file: {str(e)}")
    
    # Delete database record
    db.delete(document)
    db.commit()
    
    return None
