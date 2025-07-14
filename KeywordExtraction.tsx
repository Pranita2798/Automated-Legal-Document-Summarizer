import React, { useState, useEffect } from 'react';
import { Key, Tag, Download, AlertCircle, TrendingUp } from 'lucide-react';

interface KeywordExtractionProps {
  document: string;
  fileName: string;
}

interface Keyword {
  term: string;
  frequency: number;
  category: 'legal' | 'financial' | 'temporal' | 'general';
}

const KeywordExtraction: React.FC<KeywordExtractionProps> = ({ document, fileName }) => {
  const [keywords, setKeywords] = useState<Keyword[]>([]);
  const [keyPhrases, setKeyPhrases] = useState<string[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const extractKeywords = (text: string): Keyword[] => {
    const words = text.toLowerCase().match(/\b\w+\b/g) || [];
    const frequency: { [key: string]: number } = {};
    
    // Count word frequencies
    words.forEach(word => {
      if (word.length > 3) { // Filter out short words
        frequency[word] = (frequency[word] || 0) + 1;
      }
    });

    // Legal terms categories
    const legalTerms = ['agreement', 'contract', 'party', 'parties', 'term', 'condition', 'clause', 'provision', 'shall', 'hereby', 'whereas', 'tenant', 'landlord', 'lease', 'property', 'premises', 'liability', 'breach', 'termination', 'notice', 'rights', 'obligations', 'damages', 'remedy', 'jurisdiction', 'governing', 'binding', 'enforce', 'waiver', 'amendment'];
    
    const financialTerms = ['payment', 'rent', 'deposit', 'fee', 'cost', 'price', 'amount', 'money', 'dollar', 'compensation', 'refund', 'penalty', 'interest', 'installment', 'balance', 'due', 'payable', 'expense'];
    
    const temporalTerms = ['date', 'time', 'period', 'term', 'duration', 'month', 'year', 'day', 'week', 'annual', 'monthly', 'daily', 'deadline', 'expiration', 'commencement', 'termination'];

    const categorizeKeyword = (word: string): 'legal' | 'financial' | 'temporal' | 'general' => {
      if (legalTerms.includes(word)) return 'legal';
      if (financialTerms.includes(word)) return 'financial';
      if (temporalTerms.includes(word)) return 'temporal';
      return 'general';
    };

    // Convert to keyword objects and sort by frequency
    const keywordList = Object.entries(frequency)
      .filter(([word, freq]) => freq > 1) // Only include words that appear more than once
      .map(([word, freq]) => ({
        term: word,
        frequency: freq,
        category: categorizeKeyword(word)
      }))
      .sort((a, b) => b.frequency - a.frequency)
      .slice(0, 20); // Top 20 keywords

    return keywordList;
  };

  const extractKeyPhrases = (text: string): string[] => {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const phrases: string[] = [];
    
    // Simple phrase extraction - look for common legal phrase patterns
    const phrasePatterns = [
      /\b(subject to|in accordance with|pursuant to|with respect to|in the event of|provided that|notwithstanding|for the purpose of)\b[^.!?]*[.!?]/gi,
      /\b(the parties agree|it is agreed|the tenant shall|the landlord shall|this agreement|the term of|in consideration of)\b[^.!?]*[.!?]/gi,
      /\b(including but not limited to|without limitation|among other things|for example|such as)\b[^.!?]*[.!?]/gi,
    ];

    sentences.forEach(sentence => {
      phrasePatterns.forEach(pattern => {
        const matches = sentence.match(pattern);
        if (matches) {
          matches.forEach(match => {
            const cleanPhrase = match.trim().replace(/[.!?]+$/, '');
            if (cleanPhrase.length > 20 && cleanPhrase.length < 200) {
              phrases.push(cleanPhrase);
            }
          });
        }
      });
    });

    return [...new Set(phrases)].slice(0, 10); // Remove duplicates and limit to 10
  };

  const processKeywords = async () => {
    if (!document) return;

    setIsProcessing(true);
    
    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const extractedKeywords = extractKeywords(document);
    const extractedPhrases = extractKeyPhrases(document);
    
    setKeywords(extractedKeywords);
    setKeyPhrases(extractedPhrases);
    setIsProcessing(false);
  };

  useEffect(() => {
    if (document) {
      processKeywords();
    }
  }, [document]);

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'legal': return 'bg-blue-100 text-blue-800 border-blue-200';
      case 'financial': return 'bg-green-100 text-green-800 border-green-200';
      case 'temporal': return 'bg-purple-100 text-purple-800 border-purple-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const handleDownload = () => {
    const content = `KEYWORD EXTRACTION REPORT\n\nDocument: ${fileName}\n\n` +
      `KEYWORDS:\n${keywords.map(k => `${k.term} (${k.frequency} occurrences) - ${k.category}`).join('\n')}\n\n` +
      `KEY PHRASES:\n${keyPhrases.map(p => `• ${p}`).join('\n')}`;
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${fileName.replace('.txt', '')}_keywords.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!document) {
    return (
      <div className="max-w-4xl mx-auto text-center">
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-12">
          <AlertCircle className="mx-auto h-12 w-12 text-slate-400 mb-4" />
          <h3 className="text-lg font-medium text-slate-900 mb-2">No Document Uploaded</h3>
          <p className="text-slate-600">Please upload a document first to extract keywords.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">Keyword Extraction</h2>
            <p className="text-slate-600">Key terms and phrases from: <span className="font-medium">{fileName}</span></p>
          </div>
          {keywords.length > 0 && (
            <button
              onClick={handleDownload}
              className="inline-flex items-center px-4 py-2 border border-slate-300 text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 transition-colors"
            >
              <Download className="mr-2 h-4 w-4" />
              Download Report
            </button>
          )}
        </div>
      </div>

      {isProcessing ? (
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-12 text-center">
          <TrendingUp className="mx-auto h-12 w-12 text-blue-600 mb-4 animate-pulse" />
          <h3 className="text-lg font-medium text-slate-900 mb-2">Extracting Keywords...</h3>
          <p className="text-slate-600">Analyzing document for key terms and phrases</p>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Keywords Section */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h3 className="text-lg font-medium text-slate-900 mb-4 flex items-center">
              <Key className="mr-2 h-5 w-5 text-blue-600" />
              Keywords ({keywords.length})
            </h3>
            
            {keywords.length > 0 ? (
              <div className="space-y-4">
                <div className="flex flex-wrap gap-2">
                  {keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${getCategoryColor(keyword.category)}`}
                    >
                      {keyword.term}
                      <span className="ml-2 bg-white bg-opacity-60 rounded-full px-2 py-0.5 text-xs">
                        {keyword.frequency}
                      </span>
                    </span>
                  ))}
                </div>
                
                {/* Category Legend */}
                <div className="border-t pt-4">
                  <h4 className="text-sm font-medium text-slate-700 mb-2">Categories:</h4>
                  <div className="flex flex-wrap gap-2 text-xs">
                    <span className="inline-flex items-center px-2 py-1 rounded-full bg-blue-100 text-blue-800 border border-blue-200">
                      Legal Terms
                    </span>
                    <span className="inline-flex items-center px-2 py-1 rounded-full bg-green-100 text-green-800 border border-green-200">
                      Financial Terms
                    </span>
                    <span className="inline-flex items-center px-2 py-1 rounded-full bg-purple-100 text-purple-800 border border-purple-200">
                      Temporal Terms
                    </span>
                    <span className="inline-flex items-center px-2 py-1 rounded-full bg-gray-100 text-gray-800 border border-gray-200">
                      General Terms
                    </span>
                  </div>
                </div>
              </div>
            ) : (
              <p className="text-slate-600">No keywords extracted.</p>
            )}
          </div>

          {/* Key Phrases Section */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h3 className="text-lg font-medium text-slate-900 mb-4 flex items-center">
              <Tag className="mr-2 h-5 w-5 text-green-600" />
              Key Phrases ({keyPhrases.length})
            </h3>
            
            {keyPhrases.length > 0 ? (
              <div className="space-y-3">
                {keyPhrases.map((phrase, index) => (
                  <div key={index} className="bg-slate-50 rounded-lg p-3 border-l-4 border-green-500">
                    <p className="text-slate-800 text-sm leading-relaxed">{phrase}</p>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-slate-600">No key phrases extracted.</p>
            )}
          </div>

          {/* Statistics */}
          <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <h3 className="text-lg font-medium text-slate-900 mb-4">Extraction Statistics</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-600">{keywords.length}</div>
                <div className="text-sm text-slate-600">Keywords</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-600">{keyPhrases.length}</div>
                <div className="text-sm text-slate-600">Key Phrases</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-purple-600">
                  {keywords.filter(k => k.category === 'legal').length}
                </div>
                <div className="text-sm text-slate-600">Legal Terms</div>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-600">
                  {keywords.filter(k => k.category === 'financial').length}
                </div>
                <div className="text-sm text-slate-600">Financial Terms</div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default KeywordExtraction;