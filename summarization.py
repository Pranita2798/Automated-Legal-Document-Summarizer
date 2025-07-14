"""
Legal Document Summarization Script

This script provides AI-powered summarization for legal documents using Hugging Face transformers.
Supports extractive and abstractive summarization with legal-specific optimizations.
"""

import argparse
import re
from typing import List, Dict, Any
from pathlib import Path

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers library not available. Using fallback summarization.")


class LegalDocumentSummarizer:
    """A class for summarizing legal documents using various techniques."""
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn", max_length: int = 150):
        """
        Initialize the summarizer.
        
        Args:
            model_name: Hugging Face model name for summarization
            max_length: Maximum length of generated summary
        """
        self.model_name = model_name
        self.max_length = max_length
        self.summarizer = None
        
        if TRANSFORMERS_AVAILABLE:
            try:
                self.summarizer = pipeline(
                    "summarization",
                    model=model_name,
                    tokenizer=model_name,
                    device=0 if torch.cuda.is_available() else -1
                )
            except Exception as e:
                print(f"Error loading model: {e}")
                print("Falling back to extractive summarization")
                self.summarizer = None
    
    def preprocess_legal_text(self, text: str) -> str:
        """
        Preprocess legal text for better summarization.
        
        Args:
            text: Input legal document text
            
        Returns:
            Preprocessed text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize legal citations
        text = re.sub(r'\b\d+\s+(U\.S\.)\s+\d+', '[CITATION]', text)
        text = re.sub(r'\b\d+\s+(F\.\d+d?)\s+\d+', '[CITATION]', text)
        
        # Standardize legal phrases
        text = re.sub(r'\bWHEREAS\b', 'Given that', text)
        text = re.sub(r'\bNOW, THEREFORE\b', 'Therefore', text)
        text = re.sub(r'\bIN WITNESS WHEREOF\b', 'In confirmation', text)
        
        return text.strip()
    
    def extractive_summarization(self, text: str, num_sentences: int = 5) -> str:
        """
        Perform extractive summarization using sentence scoring.
        
        Args:
            text: Input text to summarize
            num_sentences: Number of sentences to extract
            
        Returns:
            Extractive summary
        """
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip() and len(s.strip()) > 20]
        
        if len(sentences) <= num_sentences:
            return '. '.join(sentences) + '.'
        
        # Legal keywords for scoring
        legal_keywords = [
            'agreement', 'contract', 'party', 'parties', 'term', 'condition',
            'obligation', 'right', 'liability', 'breach', 'termination',
            'payment', 'consideration', 'whereas', 'therefore', 'shall',
            'landlord', 'tenant', 'lease', 'property', 'premises'
        ]
        
        # Score sentences based on legal keyword frequency
        sentence_scores = []
        for i, sentence in enumerate(sentences):
            words = sentence.lower().split()
            score = sum(1 for word in words if word in legal_keywords)
            
            # Boost score for sentences with specific patterns
            if re.search(r'\b(this agreement|the parties|it is agreed|subject to)\b', sentence.lower()):
                score += 2
            
            # Boost score for sentences with numbers/dates (often important in legal docs)
            if re.search(r'\b\d+\b', sentence):
                score += 1
            
            sentence_scores.append((sentence, score, i))
        
        # Select top sentences
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        selected_sentences = sentence_scores[:num_sentences]
        
        # Sort by original order
        selected_sentences.sort(key=lambda x: x[2])
        
        summary = '. '.join(s[0] for s in selected_sentences) + '.'
        return summary
    
    def abstractive_summarization(self, text: str) -> str:
        """
        Perform abstractive summarization using transformer model.
        
        Args:
            text: Input text to summarize
            
        Returns:
            Abstractive summary
        """
        if not self.summarizer:
            return self.extractive_summarization(text)
        
        try:
            # Chunk text if too long
            max_chunk_length = 1024
            chunks = []
            words = text.split()
            
            for i in range(0, len(words), max_chunk_length):
                chunk = ' '.join(words[i:i + max_chunk_length])
                chunks.append(chunk)
            
            # Summarize each chunk
            chunk_summaries = []
            for chunk in chunks:
                if len(chunk.strip()) > 50:  # Skip very short chunks
                    summary = self.summarizer(
                        chunk,
                        max_length=self.max_length,
                        min_length=30,
                        do_sample=False
                    )
                    chunk_summaries.append(summary[0]['summary_text'])
            
            # Combine chunk summaries
            if len(chunk_summaries) > 1:
                combined_summary = ' '.join(chunk_summaries)
                # Summarize the combined summary if it's still too long
                if len(combined_summary.split()) > self.max_length:
                    final_summary = self.summarizer(
                        combined_summary,
                        max_length=self.max_length,
                        min_length=50,
                        do_sample=False
                    )
                    return final_summary[0]['summary_text']
                return combined_summary
            else:
                return chunk_summaries[0] if chunk_summaries else "Unable to generate summary."
        
        except Exception as e:
            print(f"Error in abstractive summarization: {e}")
            return self.extractive_summarization(text)
    
    def generate_summary(self, text: str, summary_type: str = 'abstractive',
                        length: str = 'medium') -> Dict[str, Any]:
        """
        Generate a summary of the input text.
        
        Args:
            text: Input text to summarize
            summary_type: 'abstractive' or 'extractive'
            length: 'short', 'medium', or 'long'
            
        Returns:
            Dictionary containing summary and metadata
        """
        # Preprocess text
        processed_text = self.preprocess_legal_text(text)
        
        # Determine summary parameters based on length
        if length == 'short':
            num_sentences = 3
            max_length = 80
        elif length == 'medium':
            num_sentences = 5
            max_length = 150
        else:  # long
            num_sentences = 8
            max_length = 250
        
        # Generate summary
        if summary_type == 'extractive':
            summary = self.extractive_summarization(processed_text, num_sentences)
        else:
            # Temporarily adjust max_length for this summary
            original_max_length = self.max_length
            self.max_length = max_length
            summary = self.abstractive_summarization(processed_text)
            self.max_length = original_max_length
        
        # Calculate statistics
        original_words = len(text.split())
        summary_words = len(summary.split())
        compression_ratio = (original_words - summary_words) / original_words * 100
        
        return {
            'summary': summary,
            'summary_type': summary_type,
            'length': length,
            'original_words': original_words,
            'summary_words': summary_words,
            'compression_ratio': compression_ratio,
            'sentences': len(re.split(r'[.!?]+', summary))
        }
    
    def save_summary(self, summary_data: Dict[str, Any], output_path: str, original_filename: str):
        """
        Save summary to file.
        
        Args:
            summary_data: Summary data dictionary
            output_path: Path to save the output file
            original_filename: Original filename for reference
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"LEGAL DOCUMENT SUMMARY\n")
            f.write(f"{'=' * 50}\n\n")
            f.write(f"Original Document: {original_filename}\n")
            f.write(f"Summary Type: {summary_data['summary_type']}\n")
            f.write(f"Length: {summary_data['length']}\n")
            f.write(f"Original Words: {summary_data['original_words']}\n")
            f.write(f"Summary Words: {summary_data['summary_words']}\n")
            f.write(f"Compression Ratio: {summary_data['compression_ratio']:.1f}%\n")
            f.write(f"Sentences: {summary_data['sentences']}\n\n")
            f.write(f"SUMMARY:\n")
            f.write(f"{'-' * 30}\n")
            f.write(f"{summary_data['summary']}\n")


def main():
    """Main function to run the summarization script."""
    parser = argparse.ArgumentParser(description='Summarize legal documents')
    parser.add_argument('input_file', help='Input text file path')
    parser.add_argument('--output', '-o', default='summary_output.txt', help='Output file path')
    parser.add_argument('--type', '-t', choices=['abstractive', 'extractive'], 
                       default='abstractive', help='Summarization type')
    parser.add_argument('--length', '-l', choices=['short', 'medium', 'long'], 
                       default='medium', help='Summary length')
    parser.add_argument('--model', '-m', default='facebook/bart-large-cnn', 
                       help='Hugging Face model name')
    
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
    
    # Initialize summarizer
    summarizer = LegalDocumentSummarizer(model_name=args.model)
    
    # Generate summary
    print(f"Generating {args.length} {args.type} summary...")
    print(f"Input document: {args.input_file}")
    
    summary_data = summarizer.generate_summary(text, args.type, args.length)
    
    # Save results
    summarizer.save_summary(summary_data, args.output, Path(args.input_file).name)
    
    print(f"\nSummary generated successfully!")
    print(f"Original: {summary_data['original_words']} words")
    print(f"Summary: {summary_data['summary_words']} words")
    print(f"Compression: {summary_data['compression_ratio']:.1f}%")
    print(f"Output saved to: {args.output}")


if __name__ == "__main__":
    main()