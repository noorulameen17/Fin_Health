import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { companiesAPI } from '../services/api';

const Companies: React.FC = () => {
  const [companies, setCompanies] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      const response = await companiesAPI.list();
      setCompanies(response.data);
    } catch (error) {
      console.error('Error fetching companies:', error);
      setError('Failed to fetch companies');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (companyId: number, companyName: string) => {
    if (!window.confirm(`Are you sure you want to delete "${companyName}"? This action cannot be undone and will delete all associated documents and assessments.`)) {
      return;
    }

    try {
      setDeletingId(companyId);
      setError(null);
      await companiesAPI.delete(companyId);
      // Remove the company from the list
      setCompanies(companies.filter(c => c.id !== companyId));
    } catch (error: any) {
      console.error('Error deleting company:', error);
      setError(error.response?.data?.detail || 'Failed to delete company');
    } finally {
      setDeletingId(null);
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
      <div className="px-4 py-6 sm:px-0">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold text-gray-900">Companies</h1>
          <Link
            to="/companies/new"
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
          >
            + Add Company
          </Link>
        </div>

        {error && (
          <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}

        {companies.length === 0 ? (
          <div className="text-center py-12">
            <svg
              className="mx-auto h-12 w-12 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
              />
            </svg>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No companies</h3>
            <p className="mt-1 text-sm text-gray-500">Get started by creating a new company.</p>
            <div className="mt-6">
              <Link
                to="/companies/new"
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
              >
                + New Company
              </Link>
            </div>
          </div>
        ) : (
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <ul className="divide-y divide-gray-200">
              {companies.map((company) => (
                <li key={company.id} className="relative">
                  <div className="px-4 py-4 sm:px-6 hover:bg-gray-50 transition">
                    <div className="flex items-center justify-between">
                      <Link
                        to={`/companies/${company.id}`}
                        className="flex-1 min-w-0"
                      >
                        <p className="text-lg font-medium text-primary-600 truncate">
                          {company.name}
                        </p>
                        <p className="mt-1 flex items-center text-sm text-gray-500">
                          <span className="truncate">{company.industry}</span>
                        </p>
                      </Link>
                      <div className="ml-5 flex items-center space-x-3">
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          Active
                        </span>
                        <button
                          onClick={(e) => {
                            e.preventDefault();
                            handleDelete(company.id, company.name);
                          }}
                          disabled={deletingId === company.id}
                          className="p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-full transition disabled:opacity-50 disabled:cursor-not-allowed"
                          title="Delete company"
                        >
                          {deletingId === company.id ? (
                            <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                          ) : (
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                            </svg>
                          )}
                        </button>
                      </div>
                    </div>
                    <Link to={`/companies/${company.id}`} className="block">
                      <div className="mt-2 sm:flex sm:justify-between">
                        <div className="sm:flex">
                          <p className="flex items-center text-sm text-gray-500">
                            {company.email}
                          </p>
                          <p className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0 sm:ml-6">
                            {company.phone}
                          </p>
                        </div>
                        <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                          <p>
                            Created {new Date(company.created_at).toLocaleDateString()}
                          </p>
                        </div>
                      </div>
                    </Link>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
};

export default Companies;
