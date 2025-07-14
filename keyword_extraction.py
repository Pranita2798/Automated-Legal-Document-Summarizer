"""
Keyword Extraction Script for Legal Documents

This script extracts keywords and key phrases from legal documents using various NLP techniques.
Supports both statistical and AI-based approaches for legal-specific term extraction.
"""

import argparse
import re
from typing import List, Dict, Any, Set, Tuple
from pathlib import Path
from collections import Counter
import json

try:
    from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("Warning: transformers library not available. Using statistical keyword extraction.")


class LegalKeywordExtractor:
    """A class for extracting keywords and phrases from legal documents."""
    
    def __init__(self, model_name: str = "dbmdz/bert-large-cased-finetuned-conll03-english"):
        """
        Initialize the keyword extractor.
        
        Args:
            model_name: Hugging Face model name for NER
        """
        self.model_name = model_name
        self.ner_pipeline = None
        
        # Legal domain-specific terms
        self.legal_categories = {
            'contract_terms': [
                'agreement', 'contract', 'covenant', 'provision', 'clause',
                'term', 'condition', 'stipulation', 'arrangement', 'understanding'
            ],
            'parties': [
                'party', 'parties', 'plaintiff', 'defendant', 'appellant',
                'appellee', 'petitioner', 'respondent', 'landlord', 'tenant',
                'lessor', 'lessee', 'grantor', 'grantee', 'buyer', 'seller',
                'vendor', 'purchaser', 'client', 'customer'
            ],
            'legal_actions': [
                'shall', 'must', 'may', 'will', 'should', 'agree', 'covenant',
                'warrant', 'represent', 'acknowledge', 'consent', 'waive',
                'release', 'indemnify', 'defend', 'enforce', 'terminate',
                'breach', 'default', 'violate', 'comply', 'perform'
            ],
            'financial_terms': [
                'payment', 'fee', 'cost', 'expense', 'price', 'amount',
                'consideration', 'compensation', 'damages', 'penalty',
                'interest', 'rent', 'deposit', 'refund', 'reimbursement',
                'liability', 'obligation', 'debt', 'credit', 'installment'
            ],
            'temporal_terms': [
                'date', 'time', 'period', 'term', 'duration', 'deadline',
                'expiration', 'commencement', 'termination', 'renewal',
                'extension', 'notice', 'day', 'week', 'month', 'year',
                'annual', 'monthly', 'quarterly', 'immediate', 'upon'
            ],
            'property_terms': [
                'property', 'premises', 'land', 'building', 'structure',
                'real estate', 'personal property', 'asset', 'title',
                'ownership', 'possession', 'use', 'occupancy', 'access',
                'easement', 'right of way', 'boundary', 'lot', 'parcel'
            ]
        }
        
        # Initialize NER pipeline if available
        if TRANSFORMERS_AVAILABLE:
            try:
                self.ner_pipeline = pipeline(
                    "ner",
                    model=model_name,
                    tokenizer=model_name,
                    device=0 if torch.cuda.is_available() else -1,
                    aggregation_strategy="simple"
                )
            except Exception as e:
                print(f"Error loading NER model: {e}")
                self.ner_pipeline = None
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for keyword extraction.
        
        Args:
            text: Input text
            
        Returns:
            Preprocessed text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Normalize legal phrases
        text = re.sub(r'\b(WHEREAS|NOW THEREFORE|IN WITNESS WHEREOF)\b', 
                     lambda m: m.group(1).lower(), text)
        
        return text.strip()
    
    def extract_statistical_keywords(self, text: str, min_freq: int = 2, 
                                   max_keywords: int = 50) -> List[Dict[str, Any]]:
        """
        Extract keywords using statistical methods.
        
        Args:
            text: Input text
            min_freq: Minimum frequency for keyword inclusion
            max_keywords: Maximum number of keywords to return
            
        Returns:
            List of keyword dictionaries
        """
        # Tokenize and filter words
        words = re.findall(r'\b[a-zA-Z]+\b', text.lower())
        
        # Filter out common stop words and short words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to',
            'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be',
            'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did',
            'will', 'would', 'could', 'should', 'may', 'might', 'can',
            'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
            'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        }
        
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Count word frequencies
        word_freq = Counter(filtered_words)
        
        # Filter by minimum frequency
        frequent_words = {word: freq for word, freq in word_freq.items() if freq >= min_freq}
        
        # Categorize words
        keywords = []
        for word, freq in frequent_words.items():
            category = self.categorize_word(word)
            keywords.append({
                'term': word,
                'frequency': freq,
                'category': category,
                'score': freq * (2 if category != 'general' else 1)
            })
        
        # Sort by score and return top keywords
        keywords.sort(key=lambda x: x['score'], reverse=True)
        return keywords[:max_keywords]
    
    def categorize_word(self, word: str) -> str:
        """
        Categorize a word based on legal domain knowledge.
        
        Args:
            word: Word to categorize
            
        Returns:
            Category name
        """
        word_lower = word.lower()
        
        for category, terms in self.legal_categories.items():
            if word_lower in terms:
                return category
        
        return 'general'
    
    def extract_key_phrases(self, text: str, max_phrases: int = 20) -> List[str]:
        """
        Extract key phrases from text using pattern matching.
        
        Args:
            text: Input text
            max_phrases: Maximum number of phrases to return
            
        Returns:
            List of key phrases
        """
        phrases = []
        
        # Define phrase patterns
        patterns = [
            # Legal clause patterns
            r'\b(subject to|in accordance with|pursuant to|with respect to|in the event of|provided that|notwithstanding|for the purpose of)\b[^.!?]*[.!?]',
            
            # Agreement patterns
            r'\b(the parties agree|it is agreed|the tenant shall|the landlord shall|this agreement|the term of|in consideration of)\b[^.!?]*[.!?]',
            
            # Obligation patterns
            r'\b(shall be responsible for|shall maintain|shall provide|shall pay|shall deliver|shall perform|shall comply with)\b[^.!?]*[.!?]',
            
            # Condition patterns
            r'\b(if and only if|unless and until|in the event that|on condition that|provided however)\b[^.!?]*[.!?]',
            
            # Termination patterns
            r'\b(may be terminated|shall terminate|upon termination|in case of termination|termination shall)\b[^.!?]*[.!?]',
            
            # Notice patterns
            r'\b(written notice|notice shall be|upon receipt of notice|notice is hereby given)\b[^.!?]*[.!?]'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                cleaned_phrase = re.sub(r'[.!?]+$', '', match.strip())
                if 20 <= len(cleaned_phrase) <= 200:
                    phrases.append(cleaned_phrase)
        
        # Remove duplicates and return top phrases
        unique_phrases = list(dict.fromkeys(phrases))
        return unique_phrases[:max_phrases]
    
    def extract_named_entities(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract named entities using NER model.
        
        Args:
            text: Input text
            
        Returns:
            List of named entities
        """
        if not self.ner_pipeline:
            return []
        
        try:
            # Split text into chunks for processing
            max_length = 512
            chunks = []
            words = text.split()
            
            for i in range(0, len(words), max_length):
                chunk = ' '.join(words[i:i + max_length])
                chunks.append(chunk)
            
            # Process each chunk
            all_entities = []
            for chunk in chunks:
                entities = self.ner_pipeline(chunk)
                all_entities.extend(entities)
            
            # Filter and deduplicate entities
            filtered_entities = []
            seen_entities = set()
            
            for entity in all_entities:
                entity_text = entity['word'].lower()
                if entity_text not in seen_entities and len(entity_text) > 2:
                    filtered_entities.append({
                        'text': entity['word'],
                        'label': entity['entity_group'],
                        'confidence': entity['score']
                    })
                    seen_entities.add(entity_text)
            
            return filtered_entities
        
        except Exception as e:
            print(f"Error in named entity extraction: {e}")
            return []
    
    def extract_all_keywords(self, text: str) -> Dict[str, Any]:
        """
        Extract all types of keywords and phrases from text.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary containing all extracted information
        """
        processed_text = self.preprocess_text(text)
        
        # Extract statistical keywords
        keywords = self.extract_statistical_keywords(processed_text)
        
        # Extract key phrases
        phrases = self.extract_key_phrases(processed_text)
        
        # Extract named entities
        entities = self.extract_named_entities(processed_text)
        
        # Calculate statistics
        word_count = len(processed_text.split())
        unique_keywords = len(set(kw['term'] for kw in keywords))
        
        # Categorize keywords
        category_counts = {}
        for keyword in keywords:
            category = keyword['category']
            category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            'keywords': keywords,
            'key_phrases': phrases,
            'named_entities': entities,
            'statistics': {
                'total_words': word_count,
                'unique_keywords': unique_keywords,
                'total_phrases': len(phrases),
                'total_entities': len(entities),
                'category_distribution': category_counts
            }
        }
    
    def save_results(self, results: Dict[str, Any], output_path: str, original_filename: str):
        """
        Save extraction results to file.
        
        Args:
            results: Extraction results dictionary
            output_path: Path to save the output file
            original_filename: Original filename for reference
        """
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"KEYWORD EXTRACTION REPORT\n")
            f.write(f"{'=' * 50}\n\n")
            f.write(f"Document: {original_filename}\n")
            f.write(f"Analysis Date: {Path().cwd()}\n\n")
            
            # Statistics
            stats = results['statistics']
            f.write(f"STATISTICS:\n")
            f.write(f"Total Words: {stats['total_words']}\n")
            f.write(f"Unique Keywords: {stats['unique_keywords']}\n")
            f.write(f"Key Phrases: {stats['total_phrases']}\n")
            f.write(f"Named Entities: {stats['total_entities']}\n\n")
            
            # Category distribution
            f.write(f"CATEGORY DISTRIBUTION:\n")
            for category, count in stats['category_distribution'].items():
                f.write(f"  {category}: {count}\n")
            f.write(f"\n")
            
            # Keywords
            f.write(f"KEYWORDS:\n")
            f.write(f"{'-' * 30}\n")
            for keyword in results['keywords']:
                f.write(f"{keyword['term']} ({keyword['frequency']} occurrences) - {keyword['category']}\n")
            f.write(f"\n")
            
            # Key phrases
            f.write(f"KEY PHRASES:\n")
            f.write(f"{'-' * 30}\n")
            for phrase in results['key_phrases']:
                f.write(f"• {phrase}\n")
            f.write(f"\n")
            
            # Named entities
            if results['named_entities']:
                f.write(f"NAMED ENTITIES:\n")
                f.write(f"{'-' * 30}\n")
                for entity in results['named_entities']:
                    f.write(f"{entity['text']} ({entity['label']}) - {entity['confidence']:.3f}\n")
        
        # Also save as JSON
        json_path = output_path.replace('.txt', '.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)


def main():
    """Main function to run the keyword extraction script."""
    parser = argparse.ArgumentParser(description='Extract keywords from legal documents')
    parser.add_argument('input_file', help='Input text file path')
    parser.add_argument('--output', '-o', default='keywords_output.txt', help='Output file path')
    parser.add_argument('--min-freq', type=int, default=2, help='Minimum keyword frequency')
    parser.add_argument('--max-keywords', type=int, default=50, help='Maximum number of keywords')
    parser.add_argument('--model', '-m', default='dbmdz/bert-large-cased-finetuned-conll03-english',
                       help='Hugging Face NER model name')
    
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
    
    # Initialize extractor
    extractor = LegalKeywordExtractor(model_name=args.model)
    
    # Extract keywords
    print(f"Extracting keywords from: {args.input_file}")
    print(f"Using model: {args.model}")
    
    results = extractor.extract_all_keywords(text)
    
    # Save results
    extractor.save_results(results, args.output, Path(args.input_file).name)
    
    print(f"\nKeyword extraction complete!")
    print(f"Keywords found: {len(results['keywords'])}")
    print(f"Key phrases found: {len(results['key_phrases'])}")
    print(f"Named entities found: {len(results['named_entities'])}")
    print(f"Results saved to: {args.output}")
    print(f"JSON output saved to: {args.output.replace('.txt', '.json')}")


if __name__ == "__main__":
    main()