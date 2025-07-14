import React, { useState } from 'react';
import { FileText, Upload, Download, Key, Hash, Clock, FileCheck } from 'lucide-react';
import DocumentUpload from './components/DocumentUpload';
import SummaryResults from './components/SummaryResults';
import KeywordExtraction from './components/KeywordExtraction';
import TextChunking from './components/TextChunking';

function App() {
  const [document, setDocument] = useState<string>('');
  const [fileName, setFileName] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'upload' | 'chunks' | 'summary' | 'keywords'>('upload');
  const [isProcessing, setIsProcessing] = useState(false);

  const handleDocumentUpload = (text: string, name: string) => {
    setDocument(text);
    setFileName(name);
    setActiveTab('summary');
  };

  const tabs = [
    { id: 'upload', label: 'Upload Document', icon: Upload },
    { id: 'chunks', label: 'Text Chunking', icon: Hash },
    { id: 'summary', label: 'Summary', icon: FileText },
    { id: 'keywords', label: 'Keywords', icon: Key },
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-slate-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-3">
              <div className="bg-blue-600 p-2 rounded-lg">
                <FileCheck className="h-6 w-6 text-white" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-slate-900">Legal Document Summarizer</h1>
                <p className="text-sm text-slate-600">AI-powered legal document analysis</p>
              </div>
            </div>
            <div className="flex items-center space-x-2 text-sm text-slate-600">
              <Clock className="h-4 w-4" />
              <span>Instant Analysis</span>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-6">
        <div className="border-b border-slate-200">
          <nav className="-mb-px flex space-x-8">
            {tabs.map((tab) => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`group inline-flex items-center px-1 py-4 border-b-2 font-medium text-sm transition-colors ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
                  }`}
                >
                  <Icon className={`mr-2 h-4 w-4 ${
                    activeTab === tab.id ? 'text-blue-500' : 'text-slate-400 group-hover:text-slate-500'
                  }`} />
                  {tab.label}
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'upload' && (
          <DocumentUpload onDocumentUpload={handleDocumentUpload} />
        )}
        
        {activeTab === 'chunks' && (
          <TextChunking document={document} fileName={fileName} />
        )}
        
        {activeTab === 'summary' && (
          <SummaryResults 
            document={document} 
            fileName={fileName}
            isProcessing={isProcessing}
            setIsProcessing={setIsProcessing}
          />
        )}
        
        {activeTab === 'keywords' && (
          <KeywordExtraction document={document} fileName={fileName} />
        )}
      </div>
    </div>
  );
}

export default App;