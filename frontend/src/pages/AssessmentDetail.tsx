import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { useNavigate, useParams } from 'react-router-dom';
import { assessmentsAPI } from '../services/api';

interface Assessment {
  id: number;
  company_id: number;
  financial_health_score: number;
  risk_level: string;
  strengths: Array<{ point: string }>;
  weaknesses: Array<{ point: string }>;
  opportunities: Array<{ point: string }>;
  threats: Array<{ point: string }>;
  cost_optimization: Array<{ title: string; description: string }>;
  revenue_enhancement: Array<{ title: string; description: string }>;
  working_capital_tips: Array<{ title: string; description: string }>;
  tax_optimization: Array<{ title: string; description: string }>;
  recommended_products: Array<{ product_name: string; type: string; interest_range: string; benefits: string[] }>;
  executive_summary: string;
  language: string;
  created_at: string;
}

const AssessmentDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [assessment, setAssessment] = useState<Assessment | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAssessment();
  }, [id]);

  const fetchAssessment = async () => {
    try {
      setLoading(true);
      const response = await assessmentsAPI.getById(parseInt(id!));
      setAssessment(response.data);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch assessment');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (risk: string) => {
    const riskLower = risk.toLowerCase();
    if (riskLower === 'low') return 'text-green-600 bg-green-100';
    if (riskLower === 'medium') return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const getScoreColor = (score: number) => {
    if (score >= 70) return 'text-green-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
          <p className="mt-2 text-gray-600">Loading assessment...</p>
        </div>
      </div>
    );
  }

  if (error || !assessment) {
    return (
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="text-center">
          <p className="text-red-600">{error || 'Assessment not found'}</p>
          <button
            onClick={() => navigate(-1)}
            className="mt-4 text-indigo-600 hover:text-indigo-900"
          >
            ← Go Back
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
          onClick={() => navigate(-1)}
          className="text-indigo-600 hover:text-indigo-900 mb-2"
        >
          ← Back
        </button>
        <h1 className="text-3xl font-bold text-gray-900">Financial Health Assessment</h1>
        <p className="mt-1 text-sm text-gray-600">
          Assessment ID: {assessment.id} | Generated: {new Date(assessment.created_at).toLocaleDateString()}
        </p>
      </div>

      {/* Overall Score Card */}
      <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-lg shadow-lg p-8 mb-6 text-white">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold mb-2">Financial Health Score</h2>
            <div className="flex items-baseline space-x-4">
              <span className="text-6xl font-bold">{assessment.financial_health_score}</span>
              <span className="text-2xl">/100</span>
            </div>
            <p className="mt-2 text-lg">
              Risk Level: <span className={`px-3 py-1 rounded-full font-semibold ${getRiskColor(assessment.risk_level)}`}>
                {assessment.risk_level}
              </span>
            </p>
          </div>
          <div className="text-right">
            <svg className="w-32 h-32 opacity-50" fill="currentColor" viewBox="0 0 20 20">
              <path d="M2 11a1 1 0 011-1h2a1 1 0 011 1v5a1 1 0 01-1 1H3a1 1 0 01-1-1v-5zM8 7a1 1 0 011-1h2a1 1 0 011 1v9a1 1 0 01-1 1H9a1 1 0 01-1-1V7zM14 4a1 1 0 011-1h2a1 1 0 011 1v12a1 1 0 01-1 1h-2a1 1 0 01-1-1V4z" />
            </svg>
          </div>
        </div>
      </div>

      {/* Executive Summary */}
      <div className="bg-white shadow rounded-lg p-6 mb-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Executive Summary</h2>
        <div className="text-gray-700 leading-relaxed prose prose-gray max-w-none">
          <ReactMarkdown
            components={{
              p: ({ node, ...props }) => <p className="mb-4" {...props} />,
              strong: ({ node, ...props }) => <strong className="font-semibold text-gray-900" {...props} />,
              em: ({ node, ...props }) => <em className="italic" {...props} />,
              ul: ({ node, ...props }) => <ul className="list-disc pl-5 mb-4" {...props} />,
              ol: ({ node, ...props }) => <ol className="list-decimal pl-5 mb-4" {...props} />,
              li: ({ node, ...props }) => <li className="mb-1" {...props} />,
              h1: ({ node, ...props }) => <h1 className="text-2xl font-bold mb-3" {...props} />,
              h2: ({ node, ...props }) => <h2 className="text-xl font-bold mb-2" {...props} />,
              h3: ({ node, ...props }) => <h3 className="text-lg font-semibold mb-2" {...props} />,
              blockquote: ({ node, ...props }) => <blockquote className="border-l-4 border-gray-300 pl-4 italic my-4" {...props} />,
              code: ({ node, inline, ...props }: any) => 
                inline ? (
                  <code className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono" {...props} />
                ) : (
                  <code className="block bg-gray-100 p-3 rounded text-sm font-mono overflow-x-auto" {...props} />
                ),
            }}
          >
            {assessment.executive_summary}
          </ReactMarkdown>
        </div>
      </div>

      {/* SWOT Analysis */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Strengths */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-bold text-green-600 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Strengths
          </h3>
          <ul className="space-y-2">
            {assessment.strengths.map((item, index) => (
              <li key={index} className="flex items-start">
                <span className="text-green-500 mr-2 mt-1">•</span>
                <div className="text-gray-700 flex-1">
                  <ReactMarkdown>{item.point}</ReactMarkdown>
                </div>
              </li>
            ))}
          </ul>
        </div>

        {/* Weaknesses */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-bold text-red-600 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            Weaknesses
          </h3>
          <ul className="space-y-2">
            {assessment.weaknesses.map((item, index) => (
              <li key={index} className="flex items-start">
                <span className="text-red-500 mr-2 mt-1">•</span>
                <div className="text-gray-700 flex-1">
                  <ReactMarkdown>{item.point}</ReactMarkdown>
                </div>
              </li>
            ))}
          </ul>
        </div>

        {/* Opportunities */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-bold text-blue-600 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            Opportunities
          </h3>
          <ul className="space-y-2">
            {assessment.opportunities.map((item, index) => (
              <li key={index} className="flex items-start">
                <span className="text-blue-500 mr-2 mt-1">•</span>
                <div className="text-gray-700 flex-1">
                  <ReactMarkdown>{item.point}</ReactMarkdown>
                </div>
              </li>
            ))}
          </ul>
        </div>

        {/* Threats */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-bold text-orange-600 mb-4 flex items-center">
            <svg className="w-6 h-6 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            Threats
          </h3>
          <ul className="space-y-2">
            {assessment.threats.map((item, index) => (
              <li key={index} className="flex items-start">
                <span className="text-orange-500 mr-2 mt-1">•</span>
                <div className="text-gray-700 flex-1">
                  <ReactMarkdown>{item.point}</ReactMarkdown>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Recommendations */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
        {/* Cost Optimization */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">💰 Cost Optimization</h3>
          <div className="space-y-3">
            {assessment.cost_optimization.map((item, index) => (
              <div key={index} className="border-l-4 border-purple-500 pl-4">
                <h4 className="font-semibold text-gray-900">
                  <ReactMarkdown>{item.title}</ReactMarkdown>
                </h4>
                <div className="text-sm text-gray-600 mt-1">
                  <ReactMarkdown>{item.description}</ReactMarkdown>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Revenue Enhancement */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">📈 Revenue Enhancement</h3>
          <div className="space-y-3">
            {assessment.revenue_enhancement.map((item, index) => (
              <div key={index} className="border-l-4 border-green-500 pl-4">
                <h4 className="font-semibold text-gray-900">
                  <ReactMarkdown>{item.title}</ReactMarkdown>
                </h4>
                <div className="text-sm text-gray-600 mt-1">
                  <ReactMarkdown>{item.description}</ReactMarkdown>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Working Capital */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">💼 Working Capital Tips</h3>
          <div className="space-y-3">
            {assessment.working_capital_tips.map((item, index) => (
              <div key={index} className="border-l-4 border-blue-500 pl-4">
                <h4 className="font-semibold text-gray-900">
                  <ReactMarkdown>{item.title}</ReactMarkdown>
                </h4>
                <div className="text-sm text-gray-600 mt-1">
                  <ReactMarkdown>{item.description}</ReactMarkdown>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Tax Optimization */}
        <div className="bg-white shadow rounded-lg p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">🏛️ Tax Optimization</h3>
          <div className="space-y-3">
            {assessment.tax_optimization.map((item, index) => (
              <div key={index} className="border-l-4 border-indigo-500 pl-4">
                <h4 className="font-semibold text-gray-900">
                  <ReactMarkdown>{item.title}</ReactMarkdown>
                </h4>
                <div className="text-sm text-gray-600 mt-1">
                  <ReactMarkdown>{item.description}</ReactMarkdown>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Recommended Financial Products */}
      {assessment.recommended_products && assessment.recommended_products.length > 0 && (
        <div className="bg-white shadow rounded-lg p-6">
          <h2 className="text-xl font-bold text-gray-900 mb-4">🏦 Recommended Financial Products</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {assessment.recommended_products.map((product, index) => (
              <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                <h4 className="font-bold text-gray-900">{product.product_name}</h4>
                <p className="text-sm text-gray-600 mt-1">{product.type}</p>
                <p className="text-sm font-semibold text-indigo-600 mt-2">{product.interest_range}</p>
                {product.benefits && product.benefits.length > 0 && (
                  <ul className="mt-2 space-y-1">
                    {product.benefits.map((benefit, idx) => (
                      <li key={idx} className="text-xs text-gray-500 flex items-start">
                        <span className="text-green-500 mr-1">✓</span>
                        {benefit}
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default AssessmentDetail;
