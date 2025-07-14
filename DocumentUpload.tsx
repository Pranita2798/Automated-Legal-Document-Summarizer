import React, { useState, useCallback } from 'react';
import { Upload, FileText, AlertCircle, CheckCircle } from 'lucide-react';

interface DocumentUploadProps {
  onDocumentUpload: (text: string, fileName: string) => void;
}

const DocumentUpload: React.FC<DocumentUploadProps> = ({ onDocumentUpload }) => {
  const [dragActive, setDragActive] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'success' | 'error'>('idle');
  const [errorMessage, setErrorMessage] = useState('');

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  }, []);

  const handleFile = (file: File) => {
    if (file.type === 'text/plain' || file.name.endsWith('.txt')) {
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        if (text.length > 0) {
          onDocumentUpload(text, file.name);
          setUploadStatus('success');
          setErrorMessage('');
        } else {
          setUploadStatus('error');
          setErrorMessage('File appears to be empty');
        }
      };
      reader.readAsText(file);
    } else {
      setUploadStatus('error');
      setErrorMessage('Please upload a .txt file');
    }
  };

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      handleFile(files[0]);
    }
  };

  const sampleText = `SAMPLE LEGAL DOCUMENT

LEASE AGREEMENT

This Lease Agreement ("Agreement") is entered into on January 1, 2024, between ABC Properties LLC ("Landlord") and John Smith ("Tenant") for the rental of property located at 123 Main Street, Anytown, State 12345.

TERMS AND CONDITIONS:

1. TERM: This lease shall commence on January 1, 2024, and shall continue for a period of twelve (12) months, ending on December 31, 2024.

2. RENT: Tenant agrees to pay monthly rent of $1,200, due on the first day of each month. Late fees of $50 will be charged for payments received after the 5th day of the month.

3. SECURITY DEPOSIT: Tenant shall pay a security deposit of $1,200 upon signing this agreement. The deposit will be returned within 30 days of lease termination, less any damages.

4. UTILITIES: Tenant is responsible for all utilities including electricity, gas, water, and internet services.

5. MAINTENANCE: Landlord shall maintain the property in habitable condition. Tenant shall be responsible for minor repairs and maintenance.

6. TERMINATION: Either party may terminate this lease with 30 days written notice. Early termination by tenant may result in forfeiture of security deposit.

This agreement constitutes the entire agreement between the parties and may only be modified in writing signed by both parties.

Landlord: ABC Properties LLC
Tenant: John Smith
Date: January 1, 2024`;

  const handleSampleDocument = () => {
    onDocumentUpload(sampleText, 'Sample_Lease_Agreement.txt');
    setUploadStatus('success');
  };

  return (
    <div className="max-w-4xl mx-auto">
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-slate-900 mb-4">Upload Legal Document</h2>
        <p className="text-lg text-slate-600">
          Upload your legal document for AI-powered analysis, summarization, and keyword extraction
        </p>
      </div>

      {/* Upload Area */}
      <div
        className={`relative border-2 border-dashed rounded-lg p-8 transition-all duration-200 ${
          dragActive 
            ? 'border-blue-400 bg-blue-50' 
            : 'border-slate-300 bg-white hover:border-slate-400'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <div className="text-center">
          <Upload className="mx-auto h-12 w-12 text-slate-400 mb-4" />
          <h3 className="text-lg font-medium text-slate-900 mb-2">
            Drop your document here
          </h3>
          <p className="text-slate-600 mb-4">
            or click to browse files
          </p>
          
          <input
            type="file"
            accept=".txt,text/plain"
            onChange={handleFileInput}
            className="hidden"
            id="file-upload"
          />
          
          <label
            htmlFor="file-upload"
            className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 cursor-pointer transition-colors"
          >
            <FileText className="mr-2 h-5 w-5" />
            Select File
          </label>
        </div>
      </div>

      {/* Status Messages */}
      {uploadStatus === 'success' && (
        <div className="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <div className="flex items-center">
            <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
            <span className="text-green-800">Document uploaded successfully!</span>
          </div>
        </div>
      )}

      {uploadStatus === 'error' && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div className="flex items-center">
            <AlertCircle className="h-5 w-5 text-red-600 mr-2" />
            <span className="text-red-800">{errorMessage}</span>
          </div>
        </div>
      )}

      {/* Sample Document */}
      <div className="mt-8 text-center">
        <div className="border-t border-slate-200 pt-8">
          <h3 className="text-lg font-medium text-slate-900 mb-4">
            Don't have a document ready?
          </h3>
          <button
            onClick={handleSampleDocument}
            className="inline-flex items-center px-4 py-2 border border-slate-300 text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 transition-colors"
          >
            <FileText className="mr-2 h-4 w-4" />
            Try Sample Legal Document
          </button>
        </div>
      </div>

      {/* File Format Info */}
      <div className="mt-6 bg-slate-50 rounded-lg p-4">
        <h4 className="font-medium text-slate-900 mb-2">Supported Formats:</h4>
        <ul className="text-sm text-slate-600 space-y-1">
          <li>• Plain text files (.txt)</li>
          <li>• Maximum file size: 10MB</li>
          <li>• Best results with structured legal documents</li>
        </ul>
      </div>
    </div>
  );
};

export default DocumentUpload;