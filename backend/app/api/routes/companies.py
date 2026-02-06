from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import Company, IndustryType
from pydantic import BaseModel, EmailStr
from datetime import datetime

router = APIRouter()

# Pydantic schemas
class CompanyCreate(BaseModel):
    name: str
    registration_number: str
    industry: IndustryType
    email: EmailStr
    phone: str
    address: str
    gstin: str = None
    pan: str = None

class CompanyResponse(BaseModel):
    id: int
    name: str
    registration_number: str
    industry: str
    email: str
    phone: str
    created_at: datetime
    
    class Config:
        from_attributes = True

@router.post("/", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    """Create a new company"""
    
    # Check if company already exists
    existing = db.query(Company).filter(
        Company.registration_number == company.registration_number
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Company with this registration number already exists"
        )
    
    # Create new company
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    
    return db_company

@router.get("/{company_id}", response_model=CompanyResponse)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    """Get company by ID"""
    
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    return company

@router.get("/", response_model=List[CompanyResponse])
async def list_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all companies"""
    
    companies = db.query(Company).offset(skip).limit(limit).all()
    return companies

@router.put("/{company_id}", response_model=CompanyResponse)
async def update_company(company_id: int, company: CompanyCreate, db: Session = Depends(get_db)):
    """Update company information"""
    
    db_company = db.query(Company).filter(Company.id == company_id).first()
    
    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    for key, value in company.dict().items():
        setattr(db_company, key, value)
    
    db.commit()
    db.refresh(db_company)
    
    return db_company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, db: Session = Depends(get_db)):
    """Delete a company"""
    
    company = db.query(Company).filter(Company.id == company_id).first()
    
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )
    
    db.delete(company)
    db.commit()
    
    return None
