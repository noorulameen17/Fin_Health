import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { assessmentsAPI, companiesAPI } from '../services/api';

const Dashboard: React.FC = () => {
  const [stats, setStats] = useState({
    totalCompanies: 0,
    totalAssessments: 0,
    avgHealthScore: 0,
    totalDocuments: 0,
    highRiskCompanies: 0,
    pendingCompliance: 0,
  });
  const [loading, setLoading] = useState(true);
  const [recentCompanies, setRecentCompanies] = useState<any[]>([]);
  const [recentAssessments, setRecentAssessments] = useState<any[]>([]);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const companiesRes = await companiesAPI.list(0, 100);
      const companies = companiesRes.data;
      
      // Fetch all assessments
      let allAssessments: any[] = [];
      let totalHealthScore = 0;
      let companiesWithAssessments = 0;
      let highRiskCount = 0;
      
      for (const company of companies) {
        try {
          const assessmentsRes = await assessmentsAPI.getByCompany(company.id);
          const companyAssessments = assessmentsRes.data;
          allAssessments = [...allAssessments, ...companyAssessments];
          
          // Calculate stats from latest assessment
          if (companyAssessments.length > 0) {
            const latest = companyAssessments[0];
            totalHealthScore += latest.financial_health_score || 0;
            companiesWithAssessments++;
            if (latest.risk_level === 'High' || latest.risk_level === 'Critical') {
              highRiskCount++;
            }
          }
        } catch (error) {
          console.error('Error fetching assessments for company:', company.id, error);
          // Continue even if one company fails
        }
      }
      
      setRecentCompanies(companies.slice(0, 5));
      setRecentAssessments(allAssessments.slice(0, 5));
      
      const avgScore = companiesWithAssessments > 0 ? totalHealthScore / companiesWithAssessments : 0;
      
      console.log('Dashboard Stats:', {
        totalCompanies: companies.length,
        totalAssessments: allAssessments.length,
        companiesWithAssessments,
        totalHealthScore,
        avgHealthScore: avgScore,
        highRiskCompanies: highRiskCount
      });
      
      setStats({
        totalCompanies: companies.length,
        totalAssessments: allAssessments.length,
        avgHealthScore: avgScore,
        totalDocuments: 0, // Would need document count API
        highRiskCompanies: highRiskCount,
        pendingCompliance: 0, // Would need compliance API
      });
    } catch (error) {
      console.error('Error fetching dashboard data:', error);
    } finally {
      setLoading(false);
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
      {/* Header */}
      <div className="px-4 py-6 sm:px-0">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-sm text-gray-600">
          Welcome to Financial Health Assessment Tool
        </p>
      </div>

      {/* Stats */}
      <div className="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg
                  className="h-6 w-6 text-gray-400"
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
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Companies
                  </dt>
                  <dd className="text-3xl font-semibold text-gray-900">
                    {stats.totalCompanies}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg
                  className="h-6 w-6 text-gray-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Total Assessments
                  </dt>
                  <dd className="text-3xl font-semibold text-gray-900">
                    {stats.totalAssessments}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg
                  className="h-6 w-6 text-green-500"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"
                  />
                </svg>
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    Avg Health Score
                  </dt>
                  <dd className="text-3xl font-semibold text-gray-900">
                    {stats.avgHealthScore.toFixed(1)}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white overflow-hidden shadow rounded-lg">
          <div className="p-5">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <svg
                  className="h-6 w-6 text-red-500"
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
              </div>
              <div className="ml-5 w-0 flex-1">
                <dl>
                  <dt className="text-sm font-medium text-gray-500 truncate">
                    High Risk Companies
                  </dt>
                  <dd className="text-3xl font-semibold text-gray-900">
                    {stats.highRiskCompanies}
                  </dd>
                </dl>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Companies */}
      <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-2">
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200 flex justify-between items-center">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Recent Companies
            </h3>
            <Link 
              to="/companies" 
              className="text-sm font-medium text-primary-600 hover:text-primary-700"
            >
              View All →
            </Link>
          </div>
          <ul className="divide-y divide-gray-200">
            {recentCompanies.length === 0 ? (
              <li className="px-4 py-4 sm:px-6">
                <p className="text-gray-500 text-center">
                  No companies yet. Create your first company to get started!
                </p>
              </li>
            ) : (
              recentCompanies.map((company) => (
                <li key={company.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                  <Link to={`/companies/${company.id}`}>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-primary-600">
                          {company.name}
                        </p>
                        <p className="text-sm text-gray-500">{company.industry}</p>
                      </div>
                      <div>
                        <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-green-100 text-green-800">
                          Active
                        </span>
                      </div>
                    </div>
                  </Link>
                </li>
              ))
            )}
          </ul>
        </div>

        {/* Recent Assessments */}
        <div className="bg-white shadow overflow-hidden sm:rounded-lg">
          <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
            <h3 className="text-lg leading-6 font-medium text-gray-900">
              Recent Assessments
            </h3>
          </div>
          <ul className="divide-y divide-gray-200">
            {recentAssessments.length === 0 ? (
              <li className="px-4 py-4 sm:px-6">
                <p className="text-gray-500 text-center">
                  No assessments yet. Generate your first assessment!
                </p>
              </li>
            ) : (
              recentAssessments.map((assessment) => (
                <li key={assessment.id} className="px-4 py-4 sm:px-6 hover:bg-gray-50">
                  <Link to={`/assessments/${assessment.id}`}>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-primary-600">
                          Assessment #{assessment.id}
                        </p>
                        <p className="text-xs text-gray-500">
                          {new Date(assessment.created_at).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex items-center space-x-3">
                        <div className="text-right">
                          <p className="text-sm font-semibold text-gray-900">
                            Score: {assessment.health_score}/100
                          </p>
                          <span className={`text-xs px-2 py-1 rounded-full ${
                            assessment.risk_level === 'Low' 
                              ? 'bg-green-100 text-green-800'
                              : assessment.risk_level === 'Medium'
                              ? 'bg-yellow-100 text-yellow-800'
                              : 'bg-red-100 text-red-800'
                          }`}>
                            {assessment.risk_level}
                          </span>
                        </div>
                      </div>
                    </div>
                  </Link>
                </li>
              ))
            )}
          </ul>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-lg shadow-lg p-6 text-white">
          <h3 className="text-lg font-semibold mb-2">Quick Start Guide</h3>
          <p className="text-sm mb-4">Get started with your financial assessment</p>
          <ol className="text-sm space-y-2">
            <li>1. Create a new company</li>
            <li>2. Upload financial documents</li>
            <li>3. Generate AI-powered assessment</li>
            <li>4. Review insights & recommendations</li>
            <li>5. Export investor-ready reports</li>
          </ol>
          <Link 
            to="/companies/new" 
            className="mt-4 inline-block px-4 py-2 bg-white text-blue-600 rounded-md hover:bg-gray-100 font-medium text-sm"
          >
            Create Company →
          </Link>
        </div>

        <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-lg shadow-lg p-6 text-white">
          <h3 className="text-lg font-semibold mb-2">Core Features</h3>
          <ul className="text-sm space-y-2">
            <li>✅ AI-Powered Financial Analysis</li>
            <li>✅ Credit Score Assessment</li>
            <li>✅ Risk Identification & Scoring</li>
            <li>✅ Industry Benchmarking</li>
            <li>✅ Financial Product Matching</li>
            <li>✅ Tax Compliance Tracking</li>
          </ul>
        </div>

        <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-lg shadow-lg p-6 text-white">
          <h3 className="text-lg font-semibold mb-2">Advanced Tools</h3>
          <ul className="text-sm space-y-2">
            <li>📊 Financial Forecasting (12-36 months)</li>
            <li>💰 Working Capital Optimization</li>
            <li>📈 Revenue & Expense Projections</li>
            <li>🏦 Banking Integration (Coming Soon)</li>
            <li>📄 GST Returns Integration</li>
            <li>🌐 Multilingual Support</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
