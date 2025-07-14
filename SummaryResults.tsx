import React, { useState, useEffect } from 'react';
import { FileText, Download, Copy, Loader2, AlertCircle } from 'lucide-react';

interface SummaryResultsProps {
  document: string;
  fileName: string;
  isProcessing: boolean;
  setIsProcessing: (processing: boolean) => void;
}

const SummaryResults: React.FC<SummaryResultsProps> = ({ 
  document, 
  fileName, 
  isProcessing, 
  setIsProcessing 
}) => {
  const [summary, setSummary] = useState('');
  const [summaryLength, setSummaryLength] = useState<'short' | 'medium' | 'long'>('medium');
  const [copied, setCopied] = useState(false);

  // Mock AI summarization function
  const generateSummary = (text: string, length: 'short' | 'medium' | 'long') => {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    
    let targetSentences: number;
    switch (length) {
      case 'short':
        targetSentences = Math.min(3, Math.floor(sentences.length * 0.1));
        break;
      case 'medium':
        targetSentences = Math.min(6, Math.floor(sentences.length * 0.2));
        break;
      case 'long':
        targetSentences = Math.min(10, Math.floor(sentences.length * 0.3));
        break;
    }

    // Simple extractive summarization - select key sentences
    const keyWords = ['agreement', 'contract', 'party', 'parties', 'term', 'condition', 'payment', 'rent', 'lease', 'shall', 'property', 'tenant', 'landlord'];
    
    const scoredSentences = sentences.map((sentence, index) => {
      const words = sentence.toLowerCase().split(/\s+/);
      const score = words.reduce((acc, word) => {
        return acc + (keyWords.includes(word) ? 1 : 0);
      }, 0);
      
      return { sentence: sentence.trim(), score, index };
    }).filter(item => item.sentence.length > 20);

    const selectedSentences = scoredSentences
      .sort((a, b) => b.score - a.score)
      .slice(0, targetSentences)
      .sort((a, b) => a.index - b.index)
      .map(item => item.sentence);

    return selectedSentences.join('. ') + '.';
  };

  const processSummary = async () => {
    if (!document) return;

    setIsProcessing(true);
    
    // Simulate AI processing delay
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const generatedSummary = generateSummary(document, summaryLength);
    setSummary(generatedSummary);
    setIsProcessing(false);
  };

  useEffect(() => {
    if (document) {
      processSummary();
    }
  }, [document, summaryLength]);

  const handleCopy = async () => {
    if (summary) {
      await navigator.clipboard.writeText(summary);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  const handleDownload = () => {
    if (summary) {
      const blob = new Blob([summary], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `${fileName.replace('.txt', '')}_summary.txt`;
      a.click();
      URL.revokeObjectURL(url);
    }
  };

  if (!document) {
    return (
      <div className="max-w-4xl mx-auto text-center">
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-12">
          <AlertCircle className="mx-auto h-12 w-12 text-slate-400 mb-4" />
          <h3 className="text-lg font-medium text-slate-900 mb-2">No Document Uploaded</h3>
          <p className="text-slate-600">Please upload a document first to generate a summary.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-900 mb-2">Document Summary</h2>
        <p className="text-slate-600">AI-generated summary of: <span className="font-medium">{fileName}</span></p>
      </div>

      {/* Summary Controls */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-slate-900">Summary Settings</h3>
          <div className="flex items-center space-x-2">
            <span className="text-sm text-slate-600">Length:</span>
            <select
              value={summaryLength}
              onChange={(e) => setSummaryLength(e.target.value as 'short' | 'medium' | 'long')}
              className="px-3 py-1 border border-slate-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="short">Short (3-4 sentences)</option>
              <option value="medium">Medium (5-6 sentences)</option>
              <option value="long">Long (8-10 sentences)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Summary Results */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-medium text-slate-900 flex items-center">
            <FileText className="mr-2 h-5 w-5 text-blue-600" />
            Generated Summary
          </h3>
          {summary && (
            <div className="flex items-center space-x-2">
              <button
                onClick={handleCopy}
                className="inline-flex items-center px-3 py-1 border border-slate-300 text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 transition-colors"
              >
                <Copy className="mr-1 h-4 w-4" />
                {copied ? 'Copied!' : 'Copy'}
              </button>
              <button
                onClick={handleDownload}
                className="inline-flex items-center px-3 py-1 border border-slate-300 text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 transition-colors"
              >
                <Download className="mr-1 h-4 w-4" />
                Download
              </button>
            </div>
          )}
        </div>

        {isProcessing ? (
          <div className="flex items-center justify-center py-12">
            <Loader2 className="h-8 w-8 animate-spin text-blue-600 mr-3" />
            <span className="text-lg text-slate-600">Generating summary...</span>
          </div>
        ) : summary ? (
          <div className="prose prose-slate max-w-none">
            <div className="bg-slate-50 rounded-lg p-6 border-l-4 border-blue-600">
              <p className="text-slate-800 leading-relaxed text-base">
                {summary}
              </p>
            </div>
          </div>
        ) : (
          <div className="text-center py-8">
            <p className="text-slate-600">Click "Generate Summary" to analyze your document.</p>
          </div>
        )}
      </div>

      {/* Document Statistics */}
      {document && (
        <div className="mt-6 bg-white rounded-lg shadow-sm border border-slate-200 p-6">
          <h3 className="text-lg font-medium text-slate-900 mb-4">Document Statistics</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{document.split(/\s+/).length}</div>
              <div className="text-sm text-slate-600">Words</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{document.length}</div>
              <div className="text-sm text-slate-600">Characters</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{document.split(/[.!?]+/).length}</div>
              <div className="text-sm text-slate-600">Sentences</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-blue-600">{document.split(/\n\s*\n/).length}</div>
              <div className="text-sm text-slate-600">Paragraphs</div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SummaryResults;