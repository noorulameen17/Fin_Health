import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { assessmentsAPI, companiesAPI, documentsAPI } from '../services/api';

interface Company {
  id: number;
  name: string;
  registration_number: string;
  industry: string;
  email: string;
  phone: string;
  address: string;
  gstin?: string;
  pan?: string;
  created_at: string;
}

interface Document {
  id: number;
  document_type: string;
  file_name: string;
  uploaded_at: string;
  processed: boolean;
}

interface Assessment {
  id: number;
  financial_health_score: number;
  risk_level: string;
  executive_summary: string;
  created_at: string;
}

const CompanyDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [company, setCompany] = useState<Company | null>(null);
  const [documents, setDocuments] = useState<Document[]>([]);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [documentType, setDocumentType] = useState('income_statement');
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchCompanyData();
  }, [id]);

  const fetchCompanyData = async () => {
    try {
      setLoading(true);
      setError(null);
      
      if (!id) {
        setError('No company ID provided');
        return;
      }
      
      const companyId = parseInt(id);
      
      if (isNaN(companyId)) {
        setError('Invalid company ID');
        return;
      }
      
      console.log('Fetching company data for ID:', companyId);
      
      const [companyRes, docsRes, assessmentsRes] = await Promise.all([
        companiesAPI.getById(companyId),
        documentsAPI.getByCompany(companyId),
        assessmentsAPI.getByCompany(companyId)
      ]);
      
      console.log('Company response:', companyRes.data);
      
      setCompany(companyRes.data);
      setDocuments(docsRes.data);
      setAssessments(assessmentsRes.data);
    } catch (err: any) {
      console.error('Error fetching company data:', err);
      const errorMessage = err.response?.data?.detail || err.message || 'Failed to fetch company data';
      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      setUploading(true);
      setError(null);

      // Upload the document
      const uploadResponse = await documentsAPI.upload(parseInt(id!), documentType, selectedFile);
      
      // Automatically process the uploaded document
      if (uploadResponse.data.id) {
        await documentsAPI.process(uploadResponse.data.id);
      }

      setSelectedFile(null);
      setDocumentType('income_statement');
      fetchCompanyData();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to upload document');
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDocument = async (documentId: number) => {
    if (!window.confirm('Are you sure you want to delete this document?')) {
      return;
    }

    try {
      setError(null);
      await documentsAPI.delete(documentId);
      fetchCompanyData();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete document');
    }
  };

  const handleGenerateAssessment = async () => {
    try {
      setGenerating(true);
      setError(null);
      await assessmentsAPI.generate({
        company_id: parseInt(id!),
        language: 'en'
      });
      fetchCompanyData();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to generate assessment');
    } finally {
      setGenerating(false);
    }
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          <p className="mt-2 text-gray-600">Loading company details...</p>
        </div>
      </div>
    );
  }

  if (!company) {
    return (
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="text-center py-12">
          <svg
            className="mx-auto h-12 w-12 text-red-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth="2"
              d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
            />
          </svg>
          <h3 className="mt-2 text-lg font-medium text-gray-900">Company not found</h3>
          {error && (
            <p className="mt-1 text-sm text-red-600">{error}</p>
          )}
          <p className="mt-1 text-sm text-gray-500">
            The company you're looking for doesn't exist or you don't have permission to view it.
          </p>
          <button
            onClick={() => navigate('/companies')}
            className="mt-6 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
          >
            Back to Companies
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-6">
        <button
          onClick={() => navigate('/companies')}
          className="text-indigo-600 hover:text-indigo-900 mb-2"
        >
          ← Back to Companies
        </button>
        <h1 className="text-3xl font-bold text-gray-900">{company.name}</h1>
        <p className="mt-1 text-sm text-gray-600">ID: {company.id} | Industry: {company.industry}</p>
      </div>

      {error && (
        <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Company Info */}
        <div className="lg:col-span-2 space-y-6">
          {/* Basic Information */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Company Information</h2>
            <dl className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <dt className="text-sm font-medium text-gray-500">Registration Number</dt>
                <dd className="mt-1 text-sm text-gray-900">{company.registration_number || 'N/A'}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Email</dt>
                <dd className="mt-1 text-sm text-gray-900">{company.email || 'N/A'}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Phone</dt>
                <dd className="mt-1 text-sm text-gray-900">{company.phone || 'N/A'}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">GSTIN</dt>
                <dd className="mt-1 text-sm text-gray-900">{company.gstin || 'N/A'}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">PAN</dt>
                <dd className="mt-1 text-sm text-gray-900">{company.pan || 'N/A'}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Address</dt>
                <dd className="mt-1 text-sm text-gray-900">{company.address || 'N/A'}</dd>
              </div>
            </dl>
          </div>

          {/* Documents */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Financial Documents</h2>
            
            {/* Upload Form */}
            <div className="mb-6 p-4 bg-gray-50 rounded-lg">
              <h3 className="text-sm font-medium text-gray-700 mb-3">Upload New Document</h3>
              <div className="space-y-3">
                <div>
                  <label className="block text-sm font-medium text-gray-700">Document Type</label>
                  <select
                    value={documentType}
                    onChange={(e) => setDocumentType(e.target.value)}
                    className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  >
                    <option value="income_statement">Income Statement</option>
                    <option value="balance_sheet">Balance Sheet</option>
                    <option value="cash_flow">Cash Flow Statement</option>
                    <option value="other">Other</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700">File</label>
                  <input
                    type="file"
                    onChange={handleFileChange}
                    accept=".csv,.xlsx,.xls,.pdf"
                    className="mt-1 block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-indigo-50 file:text-indigo-700 hover:file:bg-indigo-100"
                  />
                  <p className="mt-1 text-xs text-gray-500">Supported: CSV, Excel, PDF</p>
                </div>
                <button
                  onClick={handleUpload}
                  disabled={!selectedFile || uploading}
                  className="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
                >
                  {uploading ? 'Uploading...' : 'Upload Document'}
                </button>
              </div>
            </div>

            {/* Documents List */}
            <div className="space-y-2">
              {documents.length === 0 ? (
                <p className="text-sm text-gray-500">No documents uploaded yet</p>
              ) : (
                documents.map((doc) => (
                  <div key={doc.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900">{doc.file_name}</p>
                      <p className="text-xs text-gray-500">
                        Type: {doc.document_type} | Uploaded: {new Date(doc.uploaded_at).toLocaleDateString()}
                      </p>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className={`px-2 py-1 text-xs rounded ${doc.processed ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        {doc.processed ? 'Processed' : 'Pending'}
                      </span>
                      <button
                        onClick={() => handleDeleteDocument(doc.id)}
                        className="p-1 text-red-600 hover:text-red-800 hover:bg-red-50 rounded"
                        title="Delete document"
                      >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                        </svg>
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Assessments */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Financial Assessments</h2>
            
            <div className="space-y-4">
              {assessments.length === 0 ? (
                <p className="text-sm text-gray-500">No assessments generated yet</p>
              ) : (
                assessments.map((assessment) => (
                  <div key={assessment.id} className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center space-x-3">
                        <div className={`text-2xl font-bold ${assessment.financial_health_score >= 70 ? 'text-green-600' : assessment.financial_health_score >= 40 ? 'text-yellow-600' : 'text-red-600'}`}>
                          {assessment.financial_health_score}
                        </div>
                        <div>
                          <p className="text-sm font-medium text-gray-900">Health Score</p>
                          <p className="text-xs text-gray-500">Risk: {assessment.risk_level}</p>
                        </div>
                      </div>
                      <span className="text-xs text-gray-500">
                        {new Date(assessment.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="mt-3 text-sm text-gray-700">
                      <p className="font-medium mb-1">Executive Summary:</p>
                      <p className="text-gray-600">{assessment.executive_summary.substring(0, 200)}...</p>
                    </div>
                    <button
                      onClick={() => navigate(`/assessments/${assessment.id}`)}
                      className="mt-3 text-sm text-indigo-600 hover:text-indigo-900"
                    >
                      View Full Assessment →
                    </button>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        {/* Actions Sidebar */}
        <div className="space-y-6">
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Actions</h2>
            <div className="space-y-3">
              <button
                onClick={handleGenerateAssessment}
                disabled={generating || documents.length === 0}
                className="w-full bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed"
              >
                {generating ? 'Generating...' : 'Generate Assessment'}
              </button>
              {documents.length === 0 && (
                <p className="text-xs text-gray-500">Upload documents first to generate assessment</p>
              )}
              <button
                onClick={() => navigate(`/companies/edit/${id}`)}
                className="w-full bg-white border border-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-50"
              >
                Edit Company
              </button>
            </div>
          </div>

          {/* Quick Stats */}
          <div className="bg-white shadow rounded-lg p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Stats</h2>
            <dl className="space-y-3">
              <div>
                <dt className="text-sm font-medium text-gray-500">Documents</dt>
                <dd className="mt-1 text-2xl font-semibold text-gray-900">{documents.length}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Assessments</dt>
                <dd className="mt-1 text-2xl font-semibold text-gray-900">{assessments.length}</dd>
              </div>
              <div>
                <dt className="text-sm font-medium text-gray-500">Processed Docs</dt>
                <dd className="mt-1 text-2xl font-semibold text-gray-900">
                  {documents.filter(d => d.processed).length}
                </dd>
              </div>
            </dl>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CompanyDetail;
