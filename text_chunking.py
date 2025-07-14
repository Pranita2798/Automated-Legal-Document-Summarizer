"""
Text Chunking Script for Legal Document Processing

This script provides various methods for chunking legal documents into manageable segments.
Supports word-based, sentence-based, and paragraph-based chunking with overlap options.
"""

import re
import argparse
from typing import List, Dict, Any
from pathlib import Path


class TextChunker:
    """A class for chunking text documents using various methods."""
    
    def __init__(self, chunk_size: int = 200, overlap: int = 20, method: str = 'words'):
        """
        Initialize the TextChunker.
        
        Args:
            chunk_size: Size of each chunk (words/sentences/paragraphs)
            overlap: Number of units to overlap between chunks
            method: Chunking method ('words', 'sentences', 'paragraphs')
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.method = method
    
    def chunk_by_words(self, text: str) -> List[Dict[str, Any]]:
        """
        Chunk text by words.
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of dictionaries containing chunk information
        """
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), self.chunk_size - self.overlap):
            chunk_words = words[i:i + self.chunk_size]
            content = ' '.join(chunk_words)
            
            if content.strip():
                chunks.append({
                    'id': len(chunks) + 1,
                    'content': content.strip(),
                    'word_count': len(chunk_words),
                    'sentence_count': len(re.split(r'[.!?]+', content)),
                    'start_index': i,
                    'end_index': i + len(chunk_words)
                })
        
        return chunks
    
    def chunk_by_sentences(self, text: str) -> List[Dict[str, Any]]:
        """
        Chunk text by sentences.
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of dictionaries containing chunk information
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        chunks = []
        
        for i in range(0, len(sentences), self.chunk_size - self.overlap):
            chunk_sentences = sentences[i:i + self.chunk_size]
            content = '. '.join(chunk_sentences) + '.'
            
            if content.strip():
                chunks.append({
                    'id': len(chunks) + 1,
                    'content': content.strip(),
                    'word_count': len(content.split()),
                    'sentence_count': len(chunk_sentences),
                    'start_index': i,
                    'end_index': i + len(chunk_sentences)
                })
        
        return chunks
    
    def chunk_by_paragraphs(self, text: str) -> List[Dict[str, Any]]:
        """
        Chunk text by paragraphs.
        
        Args:
            text: Input text to chunk
            
        Returns:
            List of dictionaries containing chunk information
        """
        paragraphs = re.split(r'\n\s*\n', text)
        paragraphs = [p.strip() for p in paragraphs if p.strip()]
        chunks = []
        
        for i in range(0, len(paragraphs), self.chunk_size - self.overlap):
            chunk_paragraphs = paragraphs[i:i + self.chunk_size]
            content = '\n\n'.join(chunk_paragraphs)
            
            if content.strip():
                chunks.append({
                    'id': len(chunks) + 1,
                    'content': content.strip(),
                    'word_count': len(content.split()),
                    'sentence_count': len(re.split(r'[.!?]+', content)),
                    'paragraph_count': len(chunk_paragraphs),
                    'start_index': i,
                    'end_index': i + len(chunk_paragraphs)
                })
        
        return chunks
    
    def process_document(self, text: str) -> List[Dict[str, Any]]:
        """
        Process a document using the configured chunking method.
        
        Args:
            text: Input document text
            
        Returns:
            List of chunks with metadata
        """
        if self.method == 'words':
            return self.chunk_by_words(text)
        elif self.method == 'sentences':
            return self.chunk_by_sentences(text)
        elif self.method == 'paragraphs':
            return self.chunk_by_paragraphs(text)
        else:
            raise ValueError(f"Unknown chunking method: {self.method}")
    
    def save_chunks(self, chunks: List[Dict[str, Any]], output_path: str, original_filename: str):
        """
        Save chunks to a file.
        
        Args:
            chunks: List of chunk dictionaries
            output_path: Path to save the output file
            original_filename: Original filename for reference
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"TEXT CHUNKING REPORT\n")
            f.write(f"{'=' * 50}\n\n")
            f.write(f"Original Document: {original_filename}\n")
            f.write(f"Chunking Method: {self.method}\n")
            f.write(f"Chunk Size: {self.chunk_size}\n")
            f.write(f"Overlap: {self.overlap}\n")
            f.write(f"Total Chunks: {len(chunks)}\n\n")
            
            for chunk in chunks:
                f.write(f"CHUNK {chunk['id']}\n")
                f.write(f"Words: {chunk['word_count']} | Sentences: {chunk['sentence_count']}\n")
                if 'paragraph_count' in chunk:
                    f.write(f"Paragraphs: {chunk['paragraph_count']}\n")
                f.write(f"Range: {chunk['start_index']}-{chunk['end_index']}\n\n")
                f.write(f"{chunk['content']}\n\n")
                f.write(f"{'=' * 50}\n\n")


def main():
    """Main function to run the text chunking script."""
    parser = argparse.ArgumentParser(description='Chunk legal documents for processing')
    parser.add_argument('input_file', help='Input text file path')
    parser.add_argument('--output', '-o', default='chunks_output.txt', help='Output file path')
    parser.add_argument('--method', '-m', choices=['words', 'sentences', 'paragraphs'], 
                       default='words', help='Chunking method')
    parser.add_argument('--size', '-s', type=int, default=200, help='Chunk size')
    parser.add_argument('--overlap', type=int, default=20, help='Overlap between chunks')
    
    args = parser.parse_args()
    
    # Read input file
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            text = f.read()
    except FileNotFoundError:
        print(f"Error: File '{args.input_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Initialize chunker
    chunker = TextChunker(
        chunk_size=args.size,
        overlap=args.overlap,
        method=args.method
    )
    
    # Process document
    print(f"Processing document: {args.input_file}")
    print(f"Method: {args.method}, Size: {args.size}, Overlap: {args.overlap}")
    
    chunks = chunker.process_document(text)
    
    # Save results
    chunker.save_chunks(chunks, args.output, Path(args.input_file).name)
    
    print(f"\nProcessing complete!")
    print(f"Generated {len(chunks)} chunks")
    print(f"Output saved to: {args.output}")
    
    # Display statistics
    total_words = sum(chunk['word_count'] for chunk in chunks)
    avg_words = total_words / len(chunks) if chunks else 0
    
    print(f"\nStatistics:")
    print(f"Total chunks: {len(chunks)}")
    print(f"Total words: {total_words}")
    print(f"Average words per chunk: {avg_words:.1f}")


if __name__ == "__main__":
    main()