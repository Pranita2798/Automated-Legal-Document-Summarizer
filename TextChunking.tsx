import React, { useState, useEffect } from 'react';
import { Hash, Copy, Download, AlertCircle, FileText } from 'lucide-react';

interface TextChunkingProps {
  document: string;
  fileName: string;
}

interface Chunk {
  id: number;
  content: string;
  wordCount: number;
  sentences: number;
}

const TextChunking: React.FC<TextChunkingProps> = ({ document, fileName }) => {
  const [chunks, setChunks] = useState<Chunk[]>([]);
  const [chunkSize, setChunkSize] = useState<number>(200);
  const [chunkMethod, setChunkMethod] = useState<'words' | 'sentences' | 'paragraphs'>('words');
  const [overlap, setOverlap] = useState<number>(20);

  const chunkByWords = (text: string, size: number, overlapSize: number): Chunk[] => {
    const words = text.split(/\s+/);
    const chunks: Chunk[] = [];
    
    for (let i = 0; i < words.length; i += size - overlapSize) {
      const chunkWords = words.slice(i, i + size);
      const content = chunkWords.join(' ');
      
      if (content.trim().length > 0) {
        chunks.push({
          id: chunks.length + 1,
          content: content.trim(),
          wordCount: chunkWords.length,
          sentences: content.split(/[.!?]+/).filter(s => s.trim().length > 0).length
        });
      }
    }
    
    return chunks;
  };

  const chunkBySentences = (text: string, size: number, overlapSize: number): Chunk[] => {
    const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
    const chunks: Chunk[] = [];
    
    for (let i = 0; i < sentences.length; i += size - overlapSize) {
      const chunkSentences = sentences.slice(i, i + size);
      const content = chunkSentences.join('. ') + '.';
      
      if (content.trim().length > 0) {
        chunks.push({
          id: chunks.length + 1,
          content: content.trim(),
          wordCount: content.split(/\s+/).length,
          sentences: chunkSentences.length
        });
      }
    }
    
    return chunks;
  };

  const chunkByParagraphs = (text: string, size: number, overlapSize: number): Chunk[] => {
    const paragraphs = text.split(/\n\s*\n/).filter(p => p.trim().length > 0);
    const chunks: Chunk[] = [];
    
    for (let i = 0; i < paragraphs.length; i += size - overlapSize) {
      const chunkParagraphs = paragraphs.slice(i, i + size);
      const content = chunkParagraphs.join('\n\n');
      
      if (content.trim().length > 0) {
        chunks.push({
          id: chunks.length + 1,
          content: content.trim(),
          wordCount: content.split(/\s+/).length,
          sentences: content.split(/[.!?]+/).filter(s => s.trim().length > 0).length
        });
      }
    }
    
    return chunks;
  };

  const processChunks = () => {
    if (!document) return;

    let processedChunks: Chunk[] = [];
    
    switch (chunkMethod) {
      case 'words':
        processedChunks = chunkByWords(document, chunkSize, overlap);
        break;
      case 'sentences':
        processedChunks = chunkBySentences(document, chunkSize, overlap);
        break;
      case 'paragraphs':
        processedChunks = chunkByParagraphs(document, chunkSize, overlap);
        break;
    }
    
    setChunks(processedChunks);
  };

  useEffect(() => {
    processChunks();
  }, [document, chunkSize, chunkMethod, overlap]);

  const handleCopyChunk = async (content: string, chunkId: number) => {
    await navigator.clipboard.writeText(content);
    // You could add a toast notification here
  };

  const handleDownloadChunks = () => {
    const content = `TEXT CHUNKING REPORT\n\nDocument: ${fileName}\nMethod: ${chunkMethod}\nSize: ${chunkSize}\nOverlap: ${overlap}\n\n` +
      chunks.map(chunk => `CHUNK ${chunk.id}:\nWords: ${chunk.wordCount} | Sentences: ${chunk.sentences}\n\n${chunk.content}\n\n${'='.repeat(50)}\n\n`).join('');
    
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${fileName.replace('.txt', '')}_chunks.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  if (!document) {
    return (
      <div className="max-w-4xl mx-auto text-center">
        <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-12">
          <AlertCircle className="mx-auto h-12 w-12 text-slate-400 mb-4" />
          <h3 className="text-lg font-medium text-slate-900 mb-2">No Document Uploaded</h3>
          <p className="text-slate-600">Please upload a document first to perform text chunking.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-2xl font-bold text-slate-900 mb-2">Text Chunking</h2>
            <p className="text-slate-600">Break down document into manageable chunks: <span className="font-medium">{fileName}</span></p>
          </div>
          {chunks.length > 0 && (
            <button
              onClick={handleDownloadChunks}
              className="inline-flex items-center px-4 py-2 border border-slate-300 text-sm font-medium rounded-md text-slate-700 bg-white hover:bg-slate-50 transition-colors"
            >
              <Download className="mr-2 h-4 w-4" />
              Download Chunks
            </button>
          )}
        </div>
      </div>

      {/* Chunking Controls */}
      <div className="bg-white rounded-lg shadow-sm border border-slate-200 p-6 mb-6">
        <h3 className="text-lg font-medium text-slate-900 mb-4">Chunking Settings</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Method</label>
            <select
              value={chunkMethod}
              onChange={(e) => setChunkMethod(e.target.value as 'words' | 'sentences' | 'paragraphs')}
              className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="words">By Words</option>
              <option value="sentences">By Sentences</option>
              <option value="paragraphs">By Paragraphs</option>
            </select>
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">
              Size ({chunkMethod === 'words' ? 'words' : chunkMethod === 'sentences' ? 'sentences' : 'paragraphs'})
            </label>
            <input
              type="number"
              value={chunkSize}
              onChange={(e) => setChunkSize(Number(e.target.value))}
              min="1"
              max="1000"
              className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-2">Overlap</label>
            <input
              type="number"
              value={overlap}
              onChange={(e) => setOverlap(Number(e.target.value))}
              min="0"
              max={chunkSize - 1}
              className="w-full px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
        </div>
      </div>

      {/* Chunks Display */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-medium text-slate-900 flex items-center">
            <Hash className="mr-2 h-5 w-5 text-blue-600" />
            Generated Chunks ({chunks.length})
          </h3>
          <div className="text-sm text-slate-600">
            Total chunks: {chunks.length}
          </div>
        </div>

        {chunks.map((chunk) => (
          <div key={chunk.id} className="bg-white rounded-lg shadow-sm border border-slate-200 p-6">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center space-x-4">
                <h4 className="text-md font-medium text-slate-900">Chunk {chunk.id}</h4>
                <div className="flex items-center space-x-3 text-sm text-slate-600">
                  <span className="flex items-center">
                    <FileText className="mr-1 h-3 w-3" />
                    {chunk.wordCount} words
                  </span>
                  <span>{chunk.sentences} sentences</span>
                </div>
              </div>
              <button
                onClick={() => handleCopyChunk(chunk.content, chunk.id)}
                className="inline-flex items-center px-2 py-1 border border-slate-300 text-xs font-medium rounded text-slate-700 bg-white hover:bg-slate-50 transition-colors"
              >
                <Copy className="mr-1 h-3 w-3" />
                Copy
              </button>
            </div>
            
            <div className="bg-slate-50 rounded-lg p-4 border-l-4 border-blue-500">
              <p className="text-slate-800 text-sm leading-relaxed whitespace-pre-wrap">
                {chunk.content}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Statistics */}
      <div className="mt-6 bg-white rounded-lg shadow-sm border border-slate-200 p-6">
        <h3 className="text-lg font-medium text-slate-900 mb-4">Chunking Statistics</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-blue-600">{chunks.length}</div>
            <div className="text-sm text-slate-600">Total Chunks</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-green-600">
              {chunks.length > 0 ? Math.round(chunks.reduce((acc, chunk) => acc + chunk.wordCount, 0) / chunks.length) : 0}
            </div>
            <div className="text-sm text-slate-600">Avg Words/Chunk</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-purple-600">{overlap}</div>
            <div className="text-sm text-slate-600">Overlap Size</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-orange-600">{chunkMethod}</div>
            <div className="text-sm text-slate-600">Method</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TextChunking;